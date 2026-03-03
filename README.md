# 📰 News Data Pipeline & AI Recommender 2026 (Airflow + dbt + ML)

This project is a modern **End-to-End Data Engineering Pipeline** that automates the collection, storage, and intelligent analysis of news articles. Beyond ingestion, it features an **AI-powered Recommendation Engine** that suggests related news using Machine Learning.

---

## 💡 The Value: From Raw Data to Personalized Experiences
This project doesn't just "move" data; it transforms scattered internet news into a **Smart Knowledge Hub**.
* **For Users:** It provides a Netflix-like experience for news, discovering articles based on personal interest.
* **For Businesses:** It drives user engagement by automating content discovery and delivering high-quality, cleaned data for downstream applications (Dashboards, Mobile Apps, or AI Bots).

---

## 🏗️ Architecture & Tools

* **Orchestration:** Apache Airflow (Dockerized) to manage complex task dependencies.
* **Ingestion:** Python-based engine fetching real-time data from News APIs.
* **Multi-Tier Storage:**
    * **NoSQL (MongoDB):** Raw JSON storage for flexible API responses.
    * **Object Storage (MinIO):** Data lake simulation for long-term archiving.
    * **RDBMS (PostgreSQL):** Structured warehouse for clean data.
* **Transformation:** **dbt (data build tool)** for incremental SQL modeling in the `analytics` schema.
* **AI Layer:** **Recommendation Service** using `scikit-learn` (TF-IDF & Cosine Similarity) to find related articles.

---

## 🛠️ Challenges & Solutions (Technical Triumphs)

During development, we solved several high-level engineering hurdles:

1.  **ML Environment in Docker:**
    * **Problem:** The recommendation service lacked mathematical libraries like `scikit-learn`.
    * **Solution:** Customized the `Dockerfile` to include `gcc` and `libpq-dev`, and pre-installed `scikit-learn` and `pandas` to ensure the AI engine runs natively in a containerized environment.

2.  **Cross-Schema Data Access:**
    * **Problem:** The AI service couldn't find the processed tables because `dbt` creates them in an `analytics` schema by default.
    * **Solution:** Refactored the SQLAlchemy queries to explicitly reference `analytics.clean_articles`, enabling seamless communication between the warehouse and the ML model.

3.  **The OpenLineage Conflict:**
    * **Problem:** `RuntimeError` due to version mismatch between Airflow 2.7.1 and OpenLineage.
    * **Solution:** Forced `apache-airflow-providers-openlineage >= 1.8.0` in the build process to stabilize the metadata tracking.

4.  **Incremental Transformation Logic:**
    * **Problem:** Inefficient full-refresh processing of MongoDB data.
    * **Solution:** Implemented **dbt Incremental Models** that only process new records, drastically reducing latency as the dataset grows.

---

## 🚀 How to Run

1.  **Setup Environment:**
    * Create a `.env` file with your `NEWS_API_KEY` and database credentials.
2.  **Initialize & Build:**
    ```bash
    docker-compose up airflow-init
    docker-compose up -d --build
    ```
3.  **Verify AI Engine:**
    ```bash
    docker logs -f recommendation_service
    ```

---

## 📈 Project Roadmap & Achievements

* [x] Integrate Airflow & Docker orchestration.
* [x] Implement **dbt Incremental Layer** (Mongo to Postgres).
* [x] **AI Integration:** Build a Content-Based Recommender Service.
* [x] Multi-tier storage (MinIO, MongoDB, Postgres).
* [x] **CI/CD via GitHub Actions** for automated testing and builds.
* [ ] Implement **Terraform** for Cloud Infrastructure (Next Step).

---

### 📍 Project Snapshot (March 2026)
* **Status:** Production-Ready Pipeline with AI capabilities.
* **Key Achievement:** Successfully processed 76+ articles with real-time similarity scoring.