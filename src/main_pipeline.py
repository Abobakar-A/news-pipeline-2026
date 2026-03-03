import os
import requests
from dotenv import load_dotenv
from src.minio_utils import save_to_minio, read_latest_from_minio
from src.mongo_utils import save_to_mongodb
from src.postgres_utils import save_to_postgres
load_dotenv()

def run_ingestion_pipeline():
    # 1. جلب البيانات من API
    api_key = os.getenv('NEWS_API_KEY')
    url = f'https://newsapi.org/v2/everything?q=technology&apiKey={api_key}'
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        # 2. حفظ في MinIO (Landing Zone)
        save_to_minio(data)
        
        # 3. قراءة أحدث ملف من MinIO لمعالجته
        articles = read_latest_from_minio()
        
        if articles:
            # 4. حفظ في MongoDB (NoSQL Storage)
            save_to_mongodb(articles)
            
            # 5. حفظ في Postgres (Relational Staging)
            save_to_postgres(articles)

if __name__ == "__main__":
    run_ingestion_pipeline()