# Housing Analytics & Data Pipeline

A Python data pipeline executed via Google Colab that cleans a massive 400MB housing dataset, restructures it into relational tables, loads it into an SQLite database, and executes complex analytical SQL workflows.

## 🛠️ Tech Stack & Tooling
* **Data Pipeline & Engineering:** Python, Pandas, CSV parsing engines
* **Database Architecture:** SQLite3, Relational SQL Query Design
* **Environment:** Google Colab, Jupyter Notebooks

## 🚀 Analytical SQL Queries Executed
The notebook contains optimization workflows resolving 10 core business data questions, including:
* **Query 1:** Filtering high-value international real estate metrics ($1M+).
* **Query 4:** Structural aggregation calculating average square-meter pricing by microhousing regions.
* **Query 6:** Advanced Window Functions computing running cumulative prices partitioned by asset tier.

## 📦 Project Structure
* `housing_analytics_pipeline.ipynb`: Core data pipeline notebook containing data engineering logic, SQLite database creation, and SQL output cells.
