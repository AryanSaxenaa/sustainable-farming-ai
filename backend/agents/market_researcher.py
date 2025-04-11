import ollama
import pandas as pd
from typing import Dict, Any
from database.query_interface import fetch_market_conditions
from datetime import datetime, timedelta

class MarketResearcher:
    def __init__(self):
        self.models = {
            'trend_analysis': 'phi',  # Using phi for trend analysis
            'demand_forecast': 'tinyllama',  # Using tinyllama for demand forecasting
            'price_prediction': 'gemma',  # Using gemma for price prediction
        }
        self._check_models()

    def _check_models(self):
        """Check if required models are available, if not use fallback model"""
        try:
            # Try to get list of available models
            available_models = [model['name'] for model in ollama.list()['models']]
            print(f"Available models: {available_models}")
            
            # Check each model and use fallback if not available
            for key, model in self.models.items():
                if model not in available_models:
                    print(f"Model {model} not found, using tinyllama as fallback")
                    self.models[key] = 'tinyllama'  # Use tinyllama as fallback
        except Exception as e:
            print(f"Error checking models: {e}")
            # If we can't check models, use tinyllama for everything
            self.models = {key: 'tinyllama' for key in self.models}

    def get_market_trends(self, region: str, crop: str) -> Dict[str, Any]:
        """Get comprehensive market analysis using available models"""
        try:
            # Fetch market data
            market_data = fetch_market_conditions(crop=crop, date_range=30)
            if market_data.empty:
                return {
                    "error": "No market data available",
                    "metrics": None
                }

            # Calculate metrics
            metrics = self._calculate_metrics(market_data)

            # Get insights from different models
            trend_analysis = self._get_trend_analysis(region, crop, metrics)
            demand_forecast = self._get_demand_forecast(region, crop, metrics)
            price_prediction = self._get_price_prediction(region, crop, metrics)

            # Combine insights
            combined_insights = self._combine_insights(
                trend_analysis,
                demand_forecast,
                price_prediction
            )

            return {
                "insights": combined_insights,
                "metrics": metrics
            }

        except Exception as e:
            print(f"Error in get_market_trends: {e}")
            return {
                "error": str(e),
                "metrics": None
            }

    def _calculate_metrics(self, market_data: pd.DataFrame) -> Dict[str, float]:
        """Calculate market metrics from the data"""
        return {
            'avg_price': market_data['market_price'].mean(),
            'avg_demand': market_data['demand_index'].mean(),
            'avg_supply': market_data['supply_index'].mean(),
            'avg_competitor_price': market_data['competitor_price'].mean(),
            'avg_weather_impact': market_data['weather_impact'].mean(),
            'trending_season': self._get_trending_season(market_data),
            'consumer_trend': self._calculate_consumer_trend(market_data)
        }

    def _get_trending_season(self, market_data: pd.DataFrame) -> str:
        """Determine the trending season based on historical data"""
        # Implementation for season analysis
        return "Summer"  # Placeholder

    def _calculate_consumer_trend(self, market_data: pd.DataFrame) -> float:
        """Calculate consumer trend index"""
        # Implementation for trend calculation
        return 0.75  # Placeholder

    def _get_trend_analysis(self, region: str, crop: str, metrics: Dict[str, float]) -> str:
        """Get trend analysis from TinyLlama model"""
        prompt = f"""
        Analyze the market trends for {crop} in {region} based on the following metrics:
        - Average Price: ${metrics['avg_price']:.2f}
        - Average Demand: {metrics['avg_demand']:.2f}
        - Average Supply: {metrics['avg_supply']:.2f}
        - Trending Season: {metrics['trending_season']}
        
        Provide insights about:
        1. Price trends and volatility
        2. Supply-demand dynamics
        3. Seasonal patterns
        4. Market opportunities
        """
        
        response = ollama.chat(
            model=self.models['trend_analysis'],
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a market trend analyst specializing in agricultural products.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )
        
        return response['message']['content']

    def _get_demand_forecast(self, region: str, crop: str, metrics: Dict[str, float]) -> str:
        """Get demand forecast from TinyLlama model"""
        prompt = f"""
        Forecast demand for {crop} in {region} based on:
        - Current Demand Index: {metrics['avg_demand']:.2f}
        - Consumer Trend: {metrics['consumer_trend']:.2f}
        - Season: {metrics['trending_season']}
        
        Provide:
        1. Short-term demand forecast
        2. Factors affecting demand
        3. Risk factors
        """
        
        response = ollama.chat(
            model=self.models['demand_forecast'],
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a demand forecasting specialist for agricultural products.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )
        
        return response['message']['content']

    def _get_price_prediction(self, region: str, crop: str, metrics: Dict[str, float]) -> str:
        """Get price prediction from TinyLlama model"""
        prompt = f"""
        Predict prices for {crop} in {region} based on:
        - Current Price: ${metrics['avg_price']:.2f}
        - Competitor Price: ${metrics['avg_competitor_price']:.2f}
        - Weather Impact: {metrics['avg_weather_impact']:.2f}
        
        Provide:
        1. Price range prediction
        2. Factors affecting price
        3. Competitor analysis
        """
        
        response = ollama.chat(
            model=self.models['price_prediction'],
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a price prediction specialist for agricultural products.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )
        
        return response['message']['content']

    def _combine_insights(self, trend: str, demand: str, price: str) -> str:
        """Combine insights from different models into a comprehensive analysis"""
        return f"""
        Market Analysis Summary:
        
        1. Trend Analysis:
        {trend}
        
        2. Demand Forecast:
        {demand}
        
        3. Price Prediction:
        {price}
        
        Recommendations:
        - Consider the seasonal trends and market dynamics
        - Monitor competitor pricing strategies
        - Adjust production based on demand forecasts
        - Implement pricing strategies based on market conditions
        """
