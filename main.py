import os
from src.collect_api import run_collection  # Adapte le nom de la fonction
from src.clean import run_cleaning          # Adapte le nom de la fonction

def main():
    print("Starting the NEO pipeline...")

    print("\n1st step : Collecting data from NASA API")
    try:
        run_collection()
    except Exception as e:
        print(f"❌ Error during data collection : {e}")
        return

    print("\n2nd step : Cleaning and Structuring Data")
    try:
        run_cleaning()
    except Exception as e:
        print(f"❌ Error during data cleaning : {e}")
        return

    print("\n✅ Pipeline completed successfully ! The files are ready in /data/processed.")

if __name__ == "__main__":
    main()