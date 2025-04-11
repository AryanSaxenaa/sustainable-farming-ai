import pandas as pd
import sqlite3

def create_database(excel_path, db_path='farming_data.db'):
    # Connect to SQLite DB
    conn = sqlite3.connect(db_path)

    # Define expected sheets and corresponding table names
    sheet_table_map = {
        'Crops': 'crops',
        'MarketPrices': 'market_prices',
        'WeatherForecast': 'weather_forecast',
        'SoilData': 'soil_data',
        'SustainabilityMetrics': 'sustainability_metrics'
    }

    for sheet_name, table_name in sheet_table_map.items():
        try:
            df = pd.read_excel(excel_path, sheet_name=sheet_name)
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"✅ Loaded {sheet_name} into table: {table_name}")
        except Exception as e:
            print(f"⚠️ Failed to load sheet '{sheet_name}': {e}")

    conn.commit()
    conn.close()
    print("\n🎉 Database created successfully!")

if __name__ == "__main__":
    # Just provide path to your Excel file here
    create_database("YOUR_EXCEL_FILE_PATH.xlsx")
