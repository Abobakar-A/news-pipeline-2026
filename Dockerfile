FROM apache/airflow:2.7.1

USER root
# تثبيت المكتبات اللازمة للبناء
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    apt-get clean

USER airflow

# تحديث pip وتثبيت المكتبات (تم إضافة scikit-learn هنا)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    pandas polars requests python-dotenv \
    scikit-learn \
    sqlalchemy \
    psycopg2-binary==2.9.9 \
    pymongo \
    apache-airflow-providers-mongo \
    apache-airflow-providers-amazon \
    "apache-airflow-providers-openlineage>=1.8.0"

# تثبيت dbt في النهاية
RUN pip install --no-cache-dir dbt-core==1.8.0 dbt-postgres==1.8.0