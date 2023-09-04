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
                section VARCHAR(255),
                subsection VARCHAR(255),
                paragraph TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP);
""")

class Database():
    def __init__(self):
        pass

    def insert(self, paper, section, subsection, paragraph):
        cursor.execute("""INSERT INTO paragraphs (paper, section, subsection, paragraph, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, NOW(), NOW());""",
                        (paper, section, subsection, paragraph))
        conn.commit()

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
    # db.insert("paper", "section", "subsection", "paragraph")
    # db.delete("paper")
    for i in range(10):
        res = db.select("paper")
        print(res)
    