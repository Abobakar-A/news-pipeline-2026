# 📰 News Data Pipeline 2026 (Airflow + dbt + Docker)

This project is a modern **Data Engineering Pipeline** that automates the collection, storage, and transformation of news articles using a multi-layered architecture. It is designed to handle raw data from APIs and transform it into a clean, query-ready format for analytics.



---

## 🏗️ Architecture & Tools

* **Orchestration:** Apache Airflow (Dockerized) to manage task dependencies.
* **Ingestion:** Python-based ingestion engine fetching data from News APIs.
* **Multi-Tier Storage Strategy:**
    * **NoSQL (MongoDB):** For flexible, raw JSON storage of API responses.
    * **Object Storage (MinIO):** For long-term archiving and data lake simulation.
    * **RDBMS (PostgreSQL):** As a structured staging area for relational data.
* **Transformation Layer:** **dbt (data build tool)** for incremental SQL modeling and data cleaning.
* **Infrastructure:** Docker Compose for local development and container orchestration.

---

## 🛠️ Challenges & Solutions (Technical Triumphs)

During the development, we solved several critical engineering challenges:

1.  **Dependency Conflict (The OpenLineage Issue):**
    * **Problem:** Encountered a `RuntimeError` because `apache-airflow` v2.10.5 was incompatible with the default `openlineage` provider v1.0.2.
    * **Solution:** Customized the `Dockerfile` to force the installation of `apache-airflow-providers-openlineage >= 1.8.0`, ensuring compatibility and a stable environment.

2.  **Container Networking & Host Resolution:**
    * **Problem:** The `dbt` container failed to communicate with the `warehouse_db` container due to a hostname mismatch (`Temporary failure in name resolution`).
    * **Solution:** Reconfigured the `profiles.yml` to use the correct Docker internal service name, aligning the dbt profile with the Docker Compose network bridge.

3.  **Incremental Transformation Logic:**
    * **Problem:** Processing all data from MongoDB to Postgres every time is inefficient.
    * **Solution:** Built a **dbt Incremental Model** that only processes new articles based on unique identifiers, significantly reducing compute time and resource usage.

---

## 🚀 How to Run

1.  **Clone the Repository:**
    ```bash
    git clone <your-repo-link>
    cd news-pipeline-2026
    ```

2.  **Initialize the Environment:**
    (This step prepares the database and creates the admin user)
    ```bash
    docker-compose up airflow-init
    ```

3.  **Launch All Services:**
    ```bash
    docker-compose up -d
    ```

4.  **Access the Dashboard:**
    * **Airflow UI:** [http://localhost:8080](http://localhost:8080) (User: `admin` / Pass: `admin`)
    * **MinIO UI:** [http://localhost:9001](http://localhost:9001)
    * **Mongo Express:** [http://localhost:8081](http://localhost:8081)

---

## 📈 Project Roadmap & Achievements

* [x] Integrate Airflow containers to run the project.
* [x] Add a **dbt layer** for incremental transformations (MongoDB to Postgres flow).
* [x] Professional README documenting challenges and architecture.
* [ ] Implement CI/CD for Docker, Terraform, and Python code (Next Step ⚡).

---

### 📍 Project Snapshot (March 2026)
* **Status:** Fully Functional End-to-End Pipeline.
* **Last Update:** Successfully processed 77 articles through the incremental dbt model.