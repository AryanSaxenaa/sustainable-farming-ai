# backend/database/query_interface.py

import sqlite3
import pandas as pd
from datetime import datetime, timedelta

DB_PATH = "farming_data.db"

def fetch_farming_conditions(crop_type=None, location=None, date_range=30):
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT * FROM farming_conditions 
    WHERE date_recorded >= date('now', ?)
    """
    params = [f'-{date_range} days']
    
    if crop_type:
        query += " AND crop_type = ?"
        params.append(crop_type)
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def fetch_market_conditions(product=None, date_range=30):
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT * FROM market_conditions 
    WHERE date_recorded >= date('now', ?)
    """
    params = [f'-{date_range} days']
    
    if product:
        query += " AND product = ?"
        params.append(product)
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def fetch_weather_data(location, date_range=7):
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT * FROM weather_forecast 
    WHERE location = ? AND date >= date('now', ?)
    ORDER BY date DESC
    """
    df = pd.read_sql_query(query, conn, params=[location, f'-{date_range} days'])
    conn.close()
    return df

def get_sustainability_metrics(crop_type, location):
    conn = sqlite3.connect(DB_PATH)
    
    # Get farming conditions
    farming_df = fetch_farming_conditions(crop_type, location)
    
    # Get market conditions
    market_df = fetch_market_conditions(crop_type)
    
    # Get weather data
    weather_df = fetch_weather_data(location)
    
    conn.close()
    
    # Calculate average metrics
    metrics = {
        'sustainability_score': farming_df['sustainability_score'].mean() if not farming_df.empty else None,
        'fertilizer_usage': farming_df['fertilizer_usage'].mean() if not farming_df.empty else None,
        'pesticide_usage': farming_df['pesticide_usage'].mean() if not farming_df.empty else None,
        'crop_yield': farming_df['crop_yield'].mean() if not farming_df.empty else None,
        'market_demand': market_df['demand_index'].mean() if not market_df.empty else None,
        'weather_impact': market_df['weather_impact_score'].mean() if not market_df.empty else None,
        'current_temperature': weather_df['temperature'].iloc[0] if not weather_df.empty else None
    }
    
    return metrics
