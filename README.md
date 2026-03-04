# 📰 News Data Pipeline & AI Recommender 2026 (Airflow + dbt + ML)

This project is a modern **End-to-End Data Engineering Pipeline** that automates the collection, storage, and intelligent analysis of news articles. Beyond ingestion, it features an **AI-powered Recommendation Engine** that suggests related news using Machine Learning.

---

## 📺 Project Demo (Watch in Action)
Click the image below to see the full pipeline execution, from **Airflow DAGs** to the **AI Recommendation Engine** on the Streamlit dashboard.

[![News Pipeline Demo](https://img.youtube.com/vi/mzweIdY7A-k/0.jpg)](https://www.youtube.com/watch?v=mzweIdY7A-k)
*Video shows real-time data ingestion, dbt transformations, and similarity scoring.*

---

## 💡 The Value: From Raw Data to Personalized Experiences
This project doesn't just "move" data; it transforms scattered internet news into a **Smart Knowledge Hub**.
* **For Users:** It provides a Netflix-like experience for news, discovering articles based on personal interest.
* **For Businesses:** It drives user engagement by automating content discovery and delivering high-quality, cleaned data for downstream applications (Dashboards, Mobile Apps, or AI Bots).
* **Live Intelligence:** The system now provides **Executive Visibility** through a real-time dashboard, turning 80+ raw articles into actionable similarity insights.

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
* **UI Layer:** **Streamlit** dashboard for real-time visualization and interaction with the AI engine.

---

## 🛠️ Challenges & Solutions (Technical Triumphs)

During development, we solved several high-level engineering hurdles:

1. **ML Environment in Docker:**
    * **Problem:** The recommendation service lacked mathematical libraries like `scikit-learn`.
    * **Solution:** Customized the `Dockerfile` to include `gcc` and `libpq-dev`, and pre-installed `scikit-learn` and `pandas` to ensure the AI engine runs natively in a containerized environment.

2. **Cross-Schema Data Access & UI Sync:**
    * **Problem:** The AI service and Streamlit couldn't find the processed tables due to schema naming mismatches.
    * **Solution:** Refactored SQLAlchemy queries and database connections to explicitly map to the **dbt-generated analytics schema**, ensuring 100% data flow accuracy from Warehouse to UI.

3. **Infrastructure & Disk Space Optimization:**
    * **Problem:** Encountered 99% disk usage due to unreleased file descriptors (ghost files) consuming 45GB+.
    * **Solution:** Used Linux diagnostic tools (`lsof`) to identify and terminate orphaned processes, reclaiming 46GB of space without system downtime.

4. **The OpenLineage Conflict:**
    * **Problem:** `RuntimeError` due to version mismatch between Airflow 2.7.1 and OpenLineage.
    * **Solution:** Forced `apache-airflow-providers-openlineage >= 1.8.0` in the build process to stabilize metadata tracking.

5. **Incremental Transformation Logic:**
    * **Problem:** Inefficient full-refresh processing of MongoDB data.
    * **Solution:** Implemented **dbt Incremental Models** that only process new records, drastically reducing latency as the dataset grows.

---

## 🚀 How to Run

1. **Setup Environment:**
    * Create a `.env` file with your `NEWS_API_KEY` and database credentials.
2. **Initialize & Build:**
    ```bash
    docker-compose up airflow-init
    docker-compose up -d --build
    ```
3. **Access Dashboard:**
    * Open `http://localhost:8501` to interact with the News Hub and AI Recommender.

---

## 📈 Project Roadmap & Achievements

* [x] Integrate Airflow & Docker orchestration.
* [x] Implement **dbt Incremental Layer** (Mongo to Postgres).
* [x] **AI Integration:** Build a Content-Based Recommender Service.
* [x] Multi-tier storage (MinIO, MongoDB, Postgres).
* [x] **Live Dashboard:** Deployed Streamlit for real-time data visualization.
* [x] **CI/CD via GitHub Actions** for automated testing and builds.
* [ ] Implement **Terraform** for Cloud Infrastructure (Next Step).

---

### 📍 Project Snapshot (Updated: March 4, 2026)
* **Status:** **Fully Operational Full-Stack Data Product.**
* **Key Achievement:** Successfully processed **80+ articles** from **13 sources** with real-time similarity scoring and professional UI visualization.