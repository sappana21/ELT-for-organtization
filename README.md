# Organizations Medallion Pipeline

A **Medallion Architecture (Bronze → Silver → Gold)** ELT pipeline built using **Databricks Delta Live Tables (DLT)**, ingesting and transforming organization data through progressively refined layers.

##  Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   BRONZE    │  →   │   SILVER    │  →   │    GOLD     │
│  Raw Data   │      │  Cleaned &  │      │  Business   │
│  (as-is)    │      │  Deduped    │      │ Aggregates  │
└─────────────┘      └─────────────┘      └─────────────┘
```

This is an **ELT** pipeline — raw data is **loaded first** (as-is into Bronze) and **transformed afterward** inside the lakehouse (Silver/Gold), rather than being transformed before loading.

| Layer | Purpose | Description |
|-------|---------|-------------|
|  **Bronze** | Raw ingestion | Streams raw CSV files from a Databricks Volume as-is, with an added `ingestion_time` column for auditability. |
|  **Silver** | Cleaning & deduplication | Selects core columns (`Organization_Id`, `Country`, `Founded`, `Number_of_employees`, `Industry`) and drops duplicate records by `Organization_Id`. |
|  **Gold** | Business-ready aggregates | Produces summary tables: country-wise org counts, industry-wise employee totals, and founding-decade distribution. |

##  Dataset

Source: `organizations-100.csv` — 100 synthetic organization records with the following columns:

`Index, Organization_Id, Name, Website, Country, Description, Founded, Industry, Number_of_employees`

##  Tech Stack

- **Databricks** (Delta Live Tables / DLT)
- **PySpark** (Structured Streaming - `readStream` / `cloudFiles` Auto Loader)
- **Delta Lake** for storage
- **Unity Catalog Volumes** for raw file landing

##  Project Structure

```
organizations-medallion-pipeline/
├── notebooks/
│   └── org_pipeline.py          # DLT pipeline: bronze, silver, gold tables
├── data/
│   └── organizations-100.csv    # Sample source data
├── README.md
└── LICENSE
```

##  Pipeline Details

### Bronze — `org_bronze`
Streams raw CSV files from a Volume using Auto Loader (`cloudFiles`), tagging each record with an `ingestion_time` timestamp. No transformations applied.

### Silver — `org_silver`
Reads from Bronze, selects core columns (`Organization_Id`, `Country`, `Founded`, `Number_of_employees`, `Industry`), and removes duplicate records by `Organization_Id`.

### Gold — Aggregate Tables
- **`org_gold_country_summary`** — organization count and average employee count per country
- **`org_gold_industry_summary`** — organization count and total employees per industry
- **`org_gold_founded_decade`** — organization count grouped by founding decade

## How to Run

1. Upload `organizations-100.csv` to a Unity Catalog Volume:
   ```
   /Volumes/<catalog>/<schema>/<volume>/organizations/
   ```
2. Create a new **DLT Pipeline** in Databricks and point it to `notebooks/org_pipeline.py`.
3. Set the pipeline mode to **Triggered** or **Continuous** as needed.
4. Run the pipeline — Bronze, Silver, and Gold tables will be created automatically in the target schema.

##  Notes

- This is a **practice / learning project** demonstrating the Medallion Architecture (ELT) pattern using Databricks DLT.
- Dataset is synthetic and used for demonstration purposes only.

##  License

This project is licensed under the MIT License.
