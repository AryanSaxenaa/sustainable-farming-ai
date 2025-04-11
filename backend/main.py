from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def read_root():
    return FileResponse('frontend/index.html')

# Import and include routers
from agents.farmer_advisor import router as farmer_router
from agents.market_researcher import router as market_router
from agents.weather_agent import router as weather_router

app.include_router(farmer_router, prefix="/api/farmer", tags=["farmer"])
app.include_router(market_router, prefix="/api/market", tags=["market"])
app.include_router(weather_router, prefix="/api/weather", tags=["weather"]) 