import pandas as pd
import sqlite3

def populate_database():
    conn = sqlite3.connect('farming_data.db')

    # Load CSVs and save as tables
    farmer_df = pd.read_csv('farmer_advisor_dataset.csv')
    market_df = pd.read_csv('market_researcher_dataset.csv')

    farmer_df.to_sql('farmer_advisor', conn, if_exists='replace', index=False)
    market_df.to_sql('market_researcher', conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()
    print("✅ Database populated successfully.")

if __name__ == '__main__':
    populate_database()
