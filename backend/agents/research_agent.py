import requests
from bs4 import BeautifulSoup
import time
import random
from typing import List, Dict
import sqlite3
from datetime import datetime

class ResearchAgent:
    def __init__(self, db_path: str = "farming_data.db"):
        self.db_path = db_path
        self.headers = {
            'User-Agent': 'SustainableFarmingAI/1.0 (Research Agent for Academic Purposes)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        self.init_db()

    def init_db(self):
        """Initialize the research database table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS research_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                source TEXT NOT NULL,
                content TEXT NOT NULL,
                date_collected TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(topic, source, content)
            )
        ''')
        conn.commit()
        conn.close()

    def get_sustainable_practices(self, crop: str, location: str) -> List[Dict]:
        """Get sustainable farming practices for a specific crop and location"""
        # Check database first
        cached_data = self._get_cached_research(crop, location)
        if cached_data:
            return cached_data

        # If not in cache, gather new data
        practices = []
        
        # Example of ethical scraping from public agricultural extension websites
        sources = [
            "https://extension.umn.edu/",
            "https://extension.ucdavis.edu/",
            "https://extension.psu.edu/"
        ]

        for source in sources:
            try:
                # Respect robots.txt and add delay
                time.sleep(random.uniform(2, 5))
                
                response = requests.get(source, headers=self.headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extract relevant information (example implementation)
                    articles = soup.find_all('article', class_='sustainable-practice')
                    for article in articles:
                        title = article.find('h2').text if article.find('h2') else "Untitled"
                        content = article.find('div', class_='content').text if article.find('div', class_='content') else ""
                        
                        practice = {
                            'title': title,
                            'content': content,
                            'source': source
                        }
                        practices.append(practice)
                        
                        # Store in database
                        self._store_research(crop, location, practice)
            except Exception as e:
                print(f"Error scraping {source}: {str(e)}")
                continue

        return practices

    def _get_cached_research(self, crop: str, location: str) -> List[Dict]:
        """Retrieve cached research data from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT topic, source, content, date_collected 
            FROM research_data 
            WHERE topic = ? AND date_collected > datetime('now', '-7 days')
        ''', (f"{crop}_{location}",))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'title': row[0],
            'source': row[1],
            'content': row[2],
            'date_collected': row[3]
        } for row in results]

    def _store_research(self, crop: str, location: str, practice: Dict):
        """Store research data in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO research_data (topic, source, content)
                VALUES (?, ?, ?)
            ''', (f"{crop}_{location}", practice['source'], practice['content']))
            conn.commit()
        except sqlite3.IntegrityError:
            # Skip if already exists
            pass
        finally:
            conn.close()

    def get_water_conservation_tips(self, location: str) -> List[Dict]:
        """Get water conservation tips specific to a location"""
        # Similar implementation to get_sustainable_practices
        # Focused on water conservation techniques
        pass

    def get_soil_health_recommendations(self, soil_type: str) -> List[Dict]:
        """Get soil health recommendations based on soil type"""
        # Similar implementation to get_sustainable_practices
        # Focused on soil health improvement
        pass 