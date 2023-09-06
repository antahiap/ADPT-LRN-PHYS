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
                paper VARCHAR(255),
                secid VARCHAR(255),
                pid VARCHAR(255),
                title VARCHAR(255),
                paragraph TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP);
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

    def insert(self, paper, secid, pid, title, text):
        cursor.execute("""
                       INSERT INTO paragraphs (paper, secid, pid, title, paragraph, created_at, updated_at)
                       VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
                        RETURNING id;""",
                        (paper, secid, pid, title, text))
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

if __name__ == "__main__":
    db = Database()
    cursor.execute("DELETE FROM paragraphs;")
    cursor.execute("DROP TABLE paragraphs;")
    conn.commit()
    # Fetch the result
    # result = cursor.fetchone()
    # input(result)
    # db.close()
    # res = db.insert("paper", "section", "paragraph", '3', '4')
    # # print(res)
    # # db.delete("paper")
    # for i in range(10):
    #     res = db.select("paper")
    #     print(res)
    