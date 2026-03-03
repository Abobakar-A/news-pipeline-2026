import psycopg2
from psycopg2.extras import execute_values
import os

def save_to_postgres(articles):
    if not articles:
        return

    # الاتصال بـ Postgres
    conn = psycopg2.connect(
        host="warehouse_db",
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
    )
    cur = conn.cursor()

    # إنشاء جدول الـ Staging (البيانات الخام قبل الـ dbt)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS staging_news (
            id SERIAL PRIMARY KEY,
            title TEXT,
            author TEXT,
            source_name TEXT,
            published_at TIMESTAMP,
            content TEXT,
            url TEXT UNIQUE,
            ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # تحويل البيانات لشكل يفهمه Postgres
    data_to_insert = [
        (
            a.get('title'),
            a.get('author'),
            a.get('source', {}).get('name'),
            a.get('publishedAt'),
            a.get('content'),
            a.get('url')
        ) for a in articles
    ]

    # الإدخال مع منع التكرار (ON CONFLICT)
    insert_query = """
        INSERT INTO staging_news (title, author, source_name, published_at, content, url)
        VALUES %s
        ON CONFLICT (url) DO NOTHING;
    """
    
    execute_values(cur, insert_query, data_to_insert)
    
    conn.commit()
    print(f"✅ [Postgres] تم مزامنة {len(data_to_insert)} مقال بنجاح.")
    cur.close()
    conn.close()