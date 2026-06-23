# Housing Analytics Pipeline & RESTful API

A hybrid data engineering infrastructure project that ingests raw property data datasets, executes a memory-efficient data cleaning and validation pipeline via Pandas, normalizes tables into localized SQLite3 database structures, and exposes structural analytics via a Flask REST API.

## 🛠️ Tech Stack & Architecture
* **Data Engineering Workflow:** Python, Pandas Dataframes (ETL)
* **Database Management:** SQLite3, Structured SQL Query Models
* **Backend Delivery API:** Flask Framework

---

## 📦 Data Pipeline Workflow (ETL)
To handle the massive 400MB+ raw text payload without hitting cloud runtime timeouts or GitHub source control storage limits, a localized processing pipeline was implemented:

1. **Extraction & Pruning:** Ingested the raw CSV using Pandas and eliminated unstructured textual features (`ad_type`, `title`, `description`, `l4`, `l5`, `l6`) to significantly optimize system memory layout.
2. **Data Integrity Filtering:** Dropped incomplete records with critical missing fields (`price`, `coordinates`, `rooms`, `surface_covered`) to protect downstream analytical integrity.
3. **Relational Schema Normalization:** Partitioned the monolithic flat data file into separate, structured relational tables (`property_details` and `property_price_details`) linked via unique property IDs.
4. **Target Loading:** Compiled the finalized clean records directly into a compressed, binary `housing_dataset.sqlite` database asset ready for production backend execution.

---

## 📁 Repository Map
```text
housing-analytics-api/
│
├── data_pipeline/
│   └── make_db.py             # Automated Pandas ETL cleaning and normalization script
│
├── database/
│   └── housing_dataset.zip    # Compressed target relational SQLite binary asset (extract before running)
│
├── app.py                      # Production Flask REST API routing server
├── requirements.txt            # Python system dependency specifications
└── README.md                   # Core portfolio documentation


## 🚀 Active Endpoints Spec

Metrics are dynamically served at the following structural routing blocks: `GET /api/v1/analytics/<query_id>`

The endpoint listens for a target integer (`1` through `10`), fetches the matching relational query, and streams the results dynamically wrapped in a responsive Bootstrap HTML interface.

### Query Cheat Sheet:

* **`/api/v1/analytics/1`** — Filters premium global property valuations ($1M+).
* **`/api/v1/analytics/2`** — Categorizes structural properties by physical footprint scale brackets.
* **`/api/v1/analytics/3`** — Analyzes symmetrical high-density bedroom/bathroom distributions in Belgrano.
* **`/api/v1/analytics/4`** — Evaluates mean asset pricing metrics per square meter by microhousing territories.
* **`/api/v1/analytics/5`** — Isolates high-value outlier listings scaling above architectural averages.
* **`/api/v1/analytics/6`** — Computes analytical rolling window totals grouped by property tier classifications.
* **`/api/v1/analytics/7`** — Aggregates total real estate surface volume metrics across active sales listings.
* **`/api/v1/analytics/8`** — Tracks high-velocity luxury historical listings within specific temporal target ranges.
* **`/api/v1/analytics/9`** — Maps top-tier yield density indicators sorted by structural property types.
* **`/api/v1/analytics/10`** — Runs market density evaluations filtering high-volume regional territories.

---

## 💾 Replicating the Pipeline Local Environment

Because the raw `HousingDataset.csv` source data payload exceeds GitHub's physical tracking limits, it is isolated from version control. To replicate this infrastructure locally:

1. Clone this repository to your local machine.
2. Ensure your original `HousingDataset.csv` source file is placed in the project root folder.
3. Execute the data pipeline engine to regenerate the database layer:
```bash
python data_pipeline/make_db.py

```


4. Extract the database file into the target directory if using the zipped asset, or allow `make_db.py` to create a fresh one.
5. Initialize the production web server layer:
```bash
python app.py

```


6. Navigate to `http://127.0.0.1:5000/` in your browser to interact with the visual dashboard.

```

```
