variable "postgres_user" { default = "abobaker" }
variable "postgres_password" { default = "password123" }
variable "postgres_db" { default = "news_db" }
variable "mongo_user" { default = "admin" }
variable "mongo_password" { default = "password123" }
variable "minio_root_user" { default = "admin" }
variable "minio_root_password" { default = "password123" }
variable "airflow_image" { default = "apache/airflow:2.7.1" }