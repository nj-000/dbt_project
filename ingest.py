import duckdb
import requests
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"
YOUR_TOKEN = os.getenv("MOTHERDUCK_TOKEN")

# CONFIGURATION: Choose which database to use
# ============================================
USE_MOTHERDUCK = True  # Set to True to use MotherDuck (cloud), False for local DuckDB

def download_and_convert_files(taxi_type):
    """Download taxi data and convert from CSV.GZ to Parquet format."""
    data_dir = Path("data") / taxi_type
    data_dir.mkdir(exist_ok=True, parents=True)
    
    for year in [2019, 2020]:
        for month in range(1, 13):
            parquet_filename = f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
            parquet_filepath = data_dir / parquet_filename
            
            if parquet_filepath.exists():
                print(f"⏭️  Skipping {parquet_filename} (already exists)")
                continue
            
            # Download CSV.gz file
            csv_gz_filename = f"{taxi_type}_tripdata_{year}-{month:02d}.csv.gz"
            csv_gz_filepath = data_dir / csv_gz_filename
            
            print(f"⬇️  Downloading {csv_gz_filename}...")
            response = requests.get(f"{BASE_URL}/{taxi_type}/{csv_gz_filename}", stream=True)
            response.raise_for_status()
            
            with open(csv_gz_filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"🔄 Converting {csv_gz_filename} to Parquet...")
            
            # FIXED: Connect to correct database based on configuration
            if USE_MOTHERDUCK:
                conn_str = f"md:taxi_rides_ny?token={YOUR_TOKEN}" if USE_MOTHERDUCK else "taxi_rides_ny.duckdb"
                con = duckdb.connect(conn_str)
                print(f"   (Using MotherDuck)")
            else:
                con = duckdb.connect("taxi_rides_ny.duckdb")
                print(f"   (Using local DuckDB)")
            con.execute("CREATE SCHEMA IF NOT EXISTS prod")
            con.execute(f"""
                COPY (SELECT * FROM read_csv_auto('{csv_gz_filepath}'))
                TO '{parquet_filepath}' (FORMAT PARQUET)
            """)
            con.close()
            
            # Remove the CSV.gz file to save space
            csv_gz_filepath.unlink()
            print(f"✅ Completed {parquet_filename}")

def update_gitignore():
    """Add data/ directory to .gitignore if not already present."""
    gitignore_path = Path(".gitignore")
    content = gitignore_path.read_text() if gitignore_path.exists() else ""
    
    if 'data/' not in content:
        with open(gitignore_path, 'a') as f:
            f.write('\n# Data directory\ndata/\n' if content else '# Data directory\ndata/\n')
        print("📝 Updated .gitignore to exclude data/ directory")

if __name__ == "__main__":
    print("=" * 60)
    print("📥 NYC TAXI DATA INGESTION")
    print("=" * 60)
    print(f"Database: {'MotherDuck (Cloud)' if USE_MOTHERDUCK else 'Local DuckDB'}")
    print()
    
    # Update .gitignore
    update_gitignore()
    print()
    
    # Download and convert data for both taxi types
    for taxi_type in ["yellow", "green"]:
        print(f"Processing {taxi_type} taxi data...")
        download_and_convert_files(taxi_type)
        print()
    
    # Load converted parquet files into database
    print("=" * 60)
    print("📦 LOADING DATA INTO DATABASE")
    print("=" * 60)
    
    if USE_MOTHERDUCK:
        conn_str = f"md:taxi_rides_ny?token={YOUR_TOKEN}" if USE_MOTHERDUCK else "taxi_rides_ny.duckdb"
        con = duckdb.connect(conn_str)
        db_location = "MotherDuck (md:taxi_rides_ny)"
    else:
        con = duckdb.connect("taxi_rides_ny.duckdb")
        db_location = "Local file (taxi_rides_ny.duckdb)"
    
    print(f"Connecting to: {db_location}\n")
    
    # Create prod schema
    con.execute("CREATE SCHEMA IF NOT EXISTS prod")
    
    # Load taxi data from parquet files
    for taxi_type in ["yellow", "green"]:
        print(f"Creating prod.{taxi_type}_tripdata...")
        con.execute(f"""
            CREATE OR REPLACE TABLE prod.{taxi_type}_tripdata AS
            SELECT * FROM read_parquet('data/{taxi_type}/*.parquet', union_by_name=true)
        """)
        
        # Show row count
        count = con.execute(f"SELECT COUNT(*) FROM prod.{taxi_type}_tripdata").fetchone()[0]
        print(f"✅ Loaded {count:,} rows into prod.{taxi_type}_tripdata")
    
    con.close()
    
    print()
    print("=" * 60)
    print("✅ INGESTION COMPLETE")
    print("=" * 60)
    print("Next steps:")
    print("1. Run DBT transformations: dbt build --target dev")
    print("2. Verify data: python verify_db.py")
    print("3. Open shell: duckdb taxi_rides_ny.duckdb")
    print()
