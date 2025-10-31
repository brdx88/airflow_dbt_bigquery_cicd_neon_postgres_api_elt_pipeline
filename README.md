# 🛒 E-Commerce ELT Pipeline on Airflow (Docker + Astro) Including CI using GitHub Actions

## 🧭 Overview
This project is a **local E-Commerce ELT pipeline** built on **Airflow 3.x**, powered by **Astronomer (Astro CLI)**, **dbt**, **BigQuery**, **CloudStorage**, **GitHub Actions**, and **Docker**.  
It’s designed to mimic a production-ready workflow — but fully local — for anyone who wants to understand how a modern ELT pipeline works end-to-end.

Think of this as the "developer edition" of my Cloud Composer pipeline.  
Here, you control every container, every log, every environment — right from your laptop.

---

## 🔄 Pipeline Overview
The pipeline automates the movement and transformation of e-commerce data, from raw CSVs to analytics-ready tables.

Here’s the flow:
1. **Extract:** Raw CSV data (orders, customers, products) is stored locally and uploaded to a simulated GCS bucket (or local storage path).  
2. **Load:** The data is loaded into **BigQuery** (or optionally SQLite for local testing).  
3. **Transform:** **dbt** models clean, join, and enrich the data into reporting-ready marts.  
4. **Orchestrate:** **Airflow (3.x)** manages task dependencies, scheduling, and monitoring through a local Astro environment.

All this runs inside Docker containers — clean, isolated, and reproducible.

---

## 🧰 Tech Stack
| Layer | Technology | Purpose |
|-------|-------------|----------|
| **Orchestration** | Airflow 3.x (via Astronomer CLI) | Manage and schedule data pipelines locally |
| **Containerization** | Docker | Package and run isolated environments |
| **Transformation** | dbt | Model and test data in SQL |
| **Data Warehouse** | BigQuery (or SQLite for dev) | Store and query transformed data |
| **Storage** | Local directory or GCS | Stage input data before ingestion |
| **Monitoring** | Airflow UI & dbt tests | Track pipeline health and data quality |

---

## ⚙️ How It Works
Once you spin up the containers with Astro, the pipeline unfolds in five clean stages:

1. **Startup**
   - Astro builds all Docker containers (Airflow webserver, scheduler, and PostgreSQL metadata DB).
   - Airflow UI becomes available at `http://localhost:8080`.

2. **Extract & Load**
   - Raw CSVs are moved from `data/raw/` into a temporary storage area.
   - Airflow loads these files into staging tables in BigQuery (or a local DB for testing).

3. **Transform**
   - Airflow triggers dbt models to transform staging data into marts.

4. **Data Testing**
   - dbt runs built-in tests (like `not_null`, `unique`, and referential integrity) to ensure clean output.

5. **Monitoring**
   - Check DAG status, logs, and dependencies directly from the Airflow UI.

---

## 🚀 Getting Started

### 1. Clone this repo
```bash
git clone https://github.com/yourusername/ecommerce-elt-local.git
cd ecommerce-elt-local
```

### 2. Install Astronomer CLI

Follow Astronomer’s installation guide
to set up the Astro CLI.

### 3. Start the Airflow environment
```bash 
astro dev start
```

This spins up your local Airflow 3.x environment inside Docker.

### 4. Access Airflow UI
Visit `http://localhost:8080`
 and enable the `ecommerce_elt_dag`.

### 5. Run the dbt models
Inside the dbt folder:
```bash
dbt run
dbt test
```

---

## 💭 Final Thoughts

This project is my playground for learning how to orchestrate data workflows locally — before deploying to the cloud.
It mirrors the real-world setup of Cloud Composer, but with the freedom to break, debug, and rebuild anything at will.

Running Airflow through Astro and Docker taught me how to manage dependencies cleanly and simulate production workflows without paying cloud costs.

## 🤝 Connect With Me

If you’re also exploring Airflow, dbt, or modern data pipelines — let’s connect!
- [LinkedIn](https://linkedin.com/in/brianic)

---

⭐ If this repo inspired you to spin up Airflow locally, drop a star — it helps other data folks find it too.
