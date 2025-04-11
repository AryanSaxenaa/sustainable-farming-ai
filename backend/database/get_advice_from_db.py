import sqlite3

def get_advice_from_db(location=None, soil_type=None, crop=None, budget=None, land_size=None):
    conn = sqlite3.connect('farming_data.db')
    cursor = conn.cursor()

    query = "SELECT * FROM farmer_advisor WHERE 1=1"
    params = []

    if location:
        query += " AND location LIKE ?"
        params.append(f"%{location}%")
    if soil_type:
        query += " AND soil_type LIKE ?"
        params.append(f"%{soil_type}%")
    if crop:
        query += " AND recommended_crop LIKE ?"
        params.append(f"%{crop}%")
    if budget:
        query += " AND budget <= ?"
        params.append(budget)
    if land_size:
        query += " AND land_size >= ?"
        params.append(land_size)

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    return results
