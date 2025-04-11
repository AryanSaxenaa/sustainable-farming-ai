
### scraper/market_scraper.py
import requests
from bs4 import BeautifulSoup

def get_market_data(crop_name, region):
    try:
        # Example scraping logic from Agmarknet
        url = f"https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity={crop_name}&Tx_State={region}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        tables = soup.find_all("table")
        if tables:
            return {"scraped": soup.get_text()[:500]}  # simplify for demo
        return {"error": "No table found"}
    except:
        return {"error": "Failed to fetch market data"}
