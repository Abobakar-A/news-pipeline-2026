import sys
import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# إضافة المسار لضمان رؤية المجلدات
sys.path.append('/opt/airflow')

# استيراد الدالة الرئيسية التي كتبتها أنت
from src.main_pipeline import run_ingestion_pipeline


default_args = {
    'owner': 'abobakar',
    'depends_on_past': False,
    'start_date': datetime(2026, 3, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'news_full_pipeline',
    default_args=default_args,
    description='End-to-End: API to MinIO to Mongo to Postgres to dbt',
    schedule_interval='@daily',
    catchup=False
) as dag:

    # 1. مهمة جلب البيانات وتوزيعها على المخازن الثلاثة
    ingest_data_task = PythonOperator(
        task_id='ingest_to_all_storages',
        python_callable=run_ingestion_pipeline,
    )

    # 2. مهمة dbt لتنظيف البيانات النهائية (التي أصلحنا الكود الخاص بها سابقاً)
    dbt_transform_task = BashOperator(
        task_id='dbt_transform_clean_content',
        bash_command='cd /opt/airflow/dbt_project && dbt run --profiles-dir .',
    )

    # ترتيب التنفيذ
    ingest_data_task >> dbt_transform_task