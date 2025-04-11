import sqlite3
import os
import pandas as pd
from datetime import datetime, timedelta

DB_PATH = "farming_data.db"

def init_database():
    # Remove existing database if it exists
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create farming_conditions table (from farmer_advisor_dataset)
    cursor.execute("""
    CREATE TABLE farming_conditions (
        farm_id INTEGER PRIMARY KEY,
        soil_ph FLOAT,
        soil_moisture FLOAT,
        temperature FLOAT,
        rainfall FLOAT,
        crop_type TEXT,
        fertilizer_usage FLOAT,
        pesticide_usage FLOAT,
        crop_yield FLOAT,
        sustainability_score FLOAT,
        date_recorded DATE
    )
    """)

    # Create market_conditions table (from market_researcher_dataset)
    cursor.execute("""
    CREATE TABLE market_conditions (
        market_id INTEGER PRIMARY KEY,
        product TEXT,
        market_price FLOAT,
        demand_index FLOAT,
        supply_index FLOAT,
        competitor_price FLOAT,
        economic_indicator FLOAT,
        weather_impact_score FLOAT,
        seasonal_factor TEXT,
        consumer_trend_index FLOAT,
        date_recorded DATE
    )
    """)

    # Create weather_forecast table
    cursor.execute("""
    CREATE TABLE weather_forecast (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT NOT NULL,
        date DATE NOT NULL,
        temperature FLOAT,
        humidity FLOAT,
        rainfall FLOAT,
        wind_speed FLOAT,
        conditions TEXT
    )
    """)

    # Load and insert farmer advisor data
    farmer_data = pd.read_csv('database/farmer_advisor_dataset.csv')
    farmer_data['date_recorded'] = pd.date_range(
        start=datetime.now() - timedelta(days=len(farmer_data)),
        periods=len(farmer_data)
    ).strftime('%Y-%m-%d')
    
    for _, row in farmer_data.iterrows():
        cursor.execute("""
        INSERT INTO farming_conditions (
            farm_id, soil_ph, soil_moisture, temperature, rainfall,
            crop_type, fertilizer_usage, pesticide_usage, crop_yield,
            sustainability_score, date_recorded
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row['Farm_ID'], row['Soil_pH'], row['Soil_Moisture'],
            row['Temperature_C'], row['Rainfall_mm'], row['Crop_Type'],
            row['Fertilizer_Usage_kg'], row['Pesticide_Usage_kg'],
            row['Crop_Yield_ton'], row['Sustainability_Score'],
            row['date_recorded']
        ))

    # Load and insert market researcher data
    market_data = pd.read_csv('database/market_researcher_dataset.csv')
    market_data['date_recorded'] = pd.date_range(
        start=datetime.now() - timedelta(days=len(market_data)),
        periods=len(market_data)
    ).strftime('%Y-%m-%d')
    
    for _, row in market_data.iterrows():
        cursor.execute("""
        INSERT INTO market_conditions (
            market_id, product, market_price, demand_index, supply_index,
            competitor_price, economic_indicator, weather_impact_score,
            seasonal_factor, consumer_trend_index, date_recorded
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row['Market_ID'], row['Product'], row['Market_Price_per_ton'],
            row['Demand_Index'], row['Supply_Index'],
            row['Competitor_Price_per_ton'], row['Economic_Indicator'],
            row['Weather_Impact_Score'], row['Seasonal_Factor'],
            row['Consumer_Trend_Index'], row['date_recorded']
        ))

    # Insert sample weather data for locations
    locations = ['California', 'Texas', 'Florida', 'New York', 'Washington']
    for location in locations:
        cursor.execute("""
        INSERT INTO weather_forecast (
            location, date, temperature, humidity, rainfall, wind_speed, conditions
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            location,
            datetime.now().strftime('%Y-%m-%d'),
            25.0,  # temperature
            65.0,  # humidity
            0.0,   # rainfall
            10.0,  # wind_speed
            'Sunny'  # conditions
        ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_database()
    print("Database initialized successfully with synthetic data!") 