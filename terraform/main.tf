# 1. تعريف الشبكة
resource "docker_network" "news_network" {
  name = "news_pipeline_network"
}

# 2. تعريف Volume لبيانات Postgres
resource "docker_volume" "postgres_data" {
  name = "postgres_data_terraform"
}

# 3. تعريف صورة Postgres
resource "docker_image" "postgres_image" {
  name         = "postgres:13"
  keep_locally = true
}

# 4. حاوية Postgres (Warehouse DB)
resource "docker_container" "warehouse_db_tf" {
  name  = "warehouse_db_terraform"
  image = docker_image.postgres_image.image_id

  networks_advanced {
    name = docker_network.news_network.name
  }

  env = [
    "POSTGRES_USER=${var.postgres_user}",
    "POSTGRES_PASSWORD=${var.postgres_password}",
    "POSTGRES_DB=${var.postgres_db}"
  ]

  ports {
    internal = 5432
    external = 5436
  }

  mounts {
    type   = "volume"
    target = "/var/lib/postgresql/data"
    source = docker_volume.postgres_data.name
  }
}

# 5. تعريف صورة MongoDB
resource "docker_image" "mongodb_image" {
  name         = "mongo:latest"
  keep_locally = true
}

# 6. حاوية MongoDB
resource "docker_container" "mongodb_tf" {
  name  = "mongodb_terraform"
  image = docker_image.mongodb_image.image_id

  networks_advanced {
    name = docker_network.news_network.name
  }

  ports {
    internal = 27017
    external = 27018
  }
}

# 7. تعريف صورة MinIO
resource "docker_image" "minio_image" {
  name         = "minio/minio:latest"
  keep_locally = true
}

# 8. حاوية MinIO
resource "docker_container" "minio_tf" {
  name  = "minio_terraform"
  image = docker_image.minio_image.image_id

  networks_advanced {
    name = docker_network.news_network.name
  }

  env = [
    "MINIO_ROOT_USER=${var.minio_root_user}",
    "MINIO_ROOT_PASSWORD=${var.minio_root_password}"
  ]

  command = ["server", "/data", "--console-address", ":9001"]

  ports {
    internal = 9000
    external = 9005
  }

  ports {
    internal = 9001
    external = 9006
  }
}

# 9. بناء صورة Airflow المخصصة من المجلد الأب
resource "docker_image" "airflow_image" {
  name = "custom_airflow_image:latest"
  build {
    context    = "${path.cwd}/.."
    dockerfile = "Dockerfile"
  }
}

# 10. حاوية Airflow Init
resource "docker_container" "airflow_init" {
  name  = "airflow_init_terraform"
  image = docker_image.airflow_image.name
  
  networks_advanced {
    name = docker_network.news_network.name
  }

  entrypoint = ["/bin/bash"]
  command    = ["-c", "airflow db init && airflow users create --username admin --firstname admin --lastname admin --role Admin --email admin@example.com --password admin"]

  env = [
    "AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://${var.postgres_user}:${var.postgres_password}@warehouse_db_terraform:5432/${var.postgres_db}",
    "AIRFLOW__CORE__EXECUTOR=LocalExecutor",
    "AIRFLOW__WEBSERVER__SECRET_KEY=super_secret_key_2026"
  ]
}

# 11. حاوية Airflow Webserver
resource "docker_container" "airflow_webserver" {
  name    = "airflow_webserver_terraform"
  image   = docker_image.airflow_image.name
  restart = "always"
  
  networks_advanced {
    name = docker_network.news_network.name
  }

  ports {
    internal = 8080
    external = 8080
  }

  command = ["webserver"]

  volumes {
    host_path      = "${path.cwd}/../dags"
    container_path = "/opt/airflow/dags"
  }
  volumes {
    host_path      = "${path.cwd}/../dbt_project"
    container_path = "/opt/airflow/dbt_project"
  }
  volumes {
    host_path      = "${path.cwd}/../src"
    container_path = "/opt/airflow/src"
  }

  env = [
    "AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://${var.postgres_user}:${var.postgres_password}@warehouse_db_terraform:5432/${var.postgres_db}",
    "AIRFLOW__CORE__EXECUTOR=LocalExecutor",
    "AIRFLOW__CORE__LOAD_EXAMPLES=False",
    "AIRFLOW__WEBSERVER__SECRET_KEY=super_secret_key_2026",
    # المتغيرات اللازمة لـ dbt (profiles.yml)
    "POSTGRES_USER=${var.postgres_user}",
    "POSTGRES_PASSWORD=${var.postgres_password}",
    "POSTGRES_DB=${var.postgres_db}"
  ]
}

# 12. حاوية Airflow Scheduler
resource "docker_container" "airflow_scheduler" {
  name    = "airflow_scheduler_terraform"
  image   = docker_image.airflow_image.name
  restart = "always"

  networks_advanced {
    name = docker_network.news_network.name
  }

  command = ["scheduler"]

  volumes {
    host_path      = "${path.cwd}/../dags"
    container_path = "/opt/airflow/dags"
  }
  volumes {
    host_path      = "${path.cwd}/../dbt_project"
    container_path = "/opt/airflow/dbt_project"
  }
  volumes {
    host_path      = "${path.cwd}/../src"
    container_path = "/opt/airflow/src"
  }

  env = [
    "AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://${var.postgres_user}:${var.postgres_password}@warehouse_db_terraform:5432/${var.postgres_db}",
    "AIRFLOW__CORE__EXECUTOR=LocalExecutor",
    "AIRFLOW__CORE__LOAD_EXAMPLES=False",
    "AIRFLOW__WEBSERVER__SECRET_KEY=super_secret_key_2026",
    # المتغيرات اللازمة لـ dbt (profiles.yml)
    "POSTGRES_USER=${var.postgres_user}",
    "POSTGRES_PASSWORD=${var.postgres_password}",
    "POSTGRES_DB=${var.postgres_db}"
  ]
}