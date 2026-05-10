# DBT Project with DuckDB & MotherDuck Integration

A complete data pipeline solution that extracts raw data, transforms it using dbt, and publishes analytics-ready tables to MotherDuck for real-time exploration and analysis.

## 📋 Overview

This repository demonstrates an end-to-end data engineering workflow:

1. **Extract** - Raw data extraction from (https://github.com/DataTalksClub/nyc-tlc-data/) via `ingest.py`
2. **Load** - Data loaded into DuckDB for local processing
3. **Transform** - dbt handles all data transformations and quality checks
4. **Share** - Transformed data pushed to MotherDuck for team access and exploration

The project leverages dbt best practices for modularity, testing, and version control, while providing a seamless integration with DuckDB and MotherDuck for scalable data analytics.

---

## 🏗️ Architecture Overview

```
Raw Data Source
       ↓
   ingest.py
       ↓
   DuckDB (Local)
       ↓
   dbt Transform
       ↓
   MotherDuck
       ↓
   Shared Analytics Tables
```

---

## 📊 Project Structure
 
```
.
├── models/
│   ├── staging/              # Raw data staging models
│   ├── intermediate/         # Intermediate transformations
│   └── marts/                # Final analytics tables
├── macros/                   # Reusable transformation logic
├── seeds/                    # Static reference data
├── tests/                    # Data quality tests
├── dbt_packages/             # External dbt packages
├── profiles/                 # Database configurations
│   └── profiles.yml          # DuckDB & MotherDuck connections
├── ingest.py                 # Data extraction script
├── dbt_project.yml           # dbt configuration
├── packages.yml              # Package dependencies
├── Dockerfile                # Docker image
├── docker-compose.yml        # Multi-container setup
└── Makefile                  # Development commands
```
 
---

#### Your MotherDuck Dashboard

**Screenshot: Data Tables in MotherDuck**

![Data Tables Preview](https://github.com/nj-000/dbt_project/blob/main/images/Screenshot%202026-05-10%20155938.png)

**Screenshot: Query Results**

![Query Results](https://github.com/nj-000/dbt_project/blob/main/images/Screenshot%202026-05-10%20160637.png)

---

