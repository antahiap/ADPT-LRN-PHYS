import psycopg2
import os

from dotenv import load_dotenv
load_dotenv()

conn = psycopg2.connect(database=os.getenv("FLY_POSTGRES_DATABASE"),
                        host=os.getenv("FLY_POSTGRES_HOSTNAME"),
                        user=os.getenv("FLY_POSTGRES_USER"),
                        password=os.getenv("FLY_POSTGRES_PASSWORD"),
                        port=os.getenv("FLY_POSTGRES_PROXY_PORT"))
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS paragraphs
                (
                id SERIAL PRIMARY KEY,
                paper VARCHAR(255) NOT NULL,
                secid VARCHAR(255) NOT NULL,
                pid VARCHAR(255),
                title VARCHAR(255),
                paragraph TEXT NOT NULL,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                CONSTRAINT unique_paper_section_paragraph UNIQUE (paper, section, paragraph)
                );
""")
conn.commit()

class Database():
    def __init__(self):
        pass

    def bulk_insert(self, paper, section, paragraph):
        args_str = ','.join(cursor.mogrify("(%s,%s,%s,NOW(),NOW())", x[0], x[1], x[2]) for x in zip(paper, section, paragraph))
        cursor.execute("""
                       INSERT INTO paragraphs (paper, section, paragraph, created_at, updated_at)
                       VALUES %s 
                       RETURNING id;""",
                            args_str)
        ids = cursor.fetchall()
        conn.commit()

    def insert(self, paper, section, paragraph):
        cursor.execute("""INSERT INTO paragraphs (paper, section, paragraph, created_at, updated_at)
                        VALUES (%s, %s, %s, NOW(), NOW()) RETURNING id;""",
                        (paper, section, paragraph))
        id = cursor.fetchone()[0]
        conn.commit()
        return id

    def select(self, paper):
        cursor.execute("""SELECT * FROM paragraphs WHERE paper = %s;""", (paper,))
        return(cursor.fetchall())

    def delete(self, paper):
        cursor.execute("""DELETE FROM paragraphs WHERE paper = %s;""", (paper,))
        conn.commit()

    def update(self, paper, section, subsection, paragraph):
        cursor.execute("""UPDATE paragraphs SET paragraph = %s, updated_at = NOW() WHERE paper = %s AND section = %s AND subsection = %s;""",
                        (paragraph, paper, section, subsection))
        conn.commit()

    def close(self):
        cursor.close()
        conn.close()

cursor.execute("""CREATE TABLE IF NOT EXISTS keywords
                (
                id SERIAL PRIMARY KEY,
                keyword VARCHAR(255) NOT NULL UNIQUE,
                explanation TEXT NOT NULL,
                keywords TEXT[],
                created_at TIMESTAMP,
                updated_at TIMESTAMP
                );
""")          
class Keywords():
    def __init__(self):
        pass

    def bulk_insert(self, dict):
        # dict: {"keyword1": "explanation1", "keyword2": "explanation2"}
        args_str = ','.join(cursor.mogrify("(%s,%s, NOW(), NOW())", (keyword, explanation)).decode("utf-8") for keyword, explanation in dict.items())
        cursor.execute(f"""INSERT INTO keywords (keyword, explanation, created_at, updated_at)
                            VALUES {args_str} RETURNING id;""")
        ids = cursor.fetchall()
        ids = [id[0] for id in ids]
        conn.commit()
        return ids

    def insert_explanation(self, keyword, explanation):
        try: 
            cursor.execute("""INSERT INTO keywords (keyword, explanation, created_at, updated_at)
                        VALUES (%s, %s, NOW(), NOW()) RETURNING id;""",
                        (keyword, explanation))
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            print("UniqueViolation")
            return None
        id = cursor.fetchone()[0]
        conn.commit()
        return id

    def select_multi(self, keywords):
        args_str = ','.join(f"'{keyword.lower()}'" for keyword in keywords)
        cursor.execute(f"""SELECT * FROM keywords WHERE LOWER(keyword) IN ({args_str});""")
        return(cursor.fetchall())

    def select(self, keyword):
        cursor.execute("""SELECT * FROM keywords WHERE LOWER(keyword) = LOWER(%s);""", (keyword,))
        return(cursor.fetchall())

    def select_all(self):
        cursor.execute("""SELECT * FROM keywords;""")
        return(cursor.fetchall())

    def delete(self, keyword):
        cursor.execute("""DELETE FROM keywords WHERE keyword = %s;""", (keyword,))
        conn.commit()

    def update_keywords(self, keyword, keywords):
        keywords = list(keywords)
        cursor.execute("""UPDATE keywords SET keywords = %s, updated_at = NOW() WHERE keyword = %s;""",
                        (keywords, keyword))
        conn.commit()
keyword_db = Keywords()

if __name__ == "__main__":
    db = Database()
    res = db.insert("paper", "section", "paragraph")
    print(res)
    # db.delete("paper")
    # for i in range(10):
    #     res = db.select("paper")
    #     print(res)
    