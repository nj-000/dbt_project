FROM python:3.11-slim

# Install git (required for dbt packages)
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*
    
RUN pip install \
    dbt-core \
    dbt-duckdb \
    python-dotenv

RUN mkdir -p /root/.dbt

WORKDIR /usr/app/dbt

ENV DBT_PROJECT_DIR=/usr/app/dbt
ENV DBT_PROFILES_DIR=/usr/app/dbt/profiles

ENTRYPOINT ["dbt"]