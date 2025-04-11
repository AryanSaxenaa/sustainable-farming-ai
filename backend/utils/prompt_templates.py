

### utils/prompt_templates.py
FARMER_PROMPT_TEMPLATE = """
As a sustainable farming expert, provide comprehensive advice for {crop} cultivation in {location} with {soil_type} soil.

Key Parameters:
- Location: {location}
- Crop: {crop}
- Soil Type: {soil_type}
- Season: {season}
- Water Availability: {water_availability}
- Previous Crop: {previous_crop}
- Known Pest Issues: {pest_issues}

Historical Data:
- Sustainability Score: {sustainability_score}
- Average Fertilizer Usage: {avg_fertilizer_usage} kg/ha
- Average Pesticide Usage: {avg_pesticide_usage} kg/ha
- Average Crop Yield: {avg_crop_yield} tons/ha
- Market Demand Index: {market_demand}
- Weather Impact Score: {weather_impact}
- Current Temperature: {current_temperature}°C

Please provide a structured response with the following sections:

1. Sustainable Farming Practices
   • Soil Health Management
     - Specific soil improvement techniques
     - Organic matter management
     - Nutrient balance recommendations
   • Water Conservation
     - Irrigation optimization methods
     - Rainwater harvesting techniques
     - Water recycling strategies
   • Organic Farming
     - Natural fertilizer recommendations
     - Composting methods
     - Cover cropping suggestions
   • Crop Rotation
     - Recommended rotation sequence
     - Intercropping opportunities
     - Green manure options

2. Pest Management
   • Preventive Measures
     - Cultural practices
     - Physical barriers
     - Biological controls
   • Natural Control Methods
     - Beneficial insects
     - Botanical pesticides
     - Companion planting
   • Treatment Options
     - Organic treatments
     - Biological agents
     - Mechanical controls
   • Monitoring Strategies
     - Regular inspection schedule
     - Early warning signs
     - Record keeping methods

3. Resource Optimization
   • Water Management
     - Efficient irrigation systems
     - Water scheduling
     - Conservation techniques
   • Energy Efficiency
     - Renewable energy options
     - Equipment optimization
     - Process improvements
   • Input Management
     - Fertilizer optimization
     - Seed selection
     - Equipment maintenance
   • Waste Management
     - Composting systems
     - Recycling methods
     - Byproduct utilization

4. Implementation Plan
   • Immediate Actions (Week 1)
     - Priority tasks
     - Resource allocation
     - Team assignments
   • Short-term Goals (1-3 months)
     - Monthly milestones
     - Progress indicators
     - Adjustment points
   • Long-term Strategies (6-12 months)
     - Infrastructure development
     - Capacity building
     - Market integration
   • Monitoring & Evaluation
     - Performance metrics
     - Regular assessments
     - Feedback mechanisms

Focus on:
- Sustainable and eco-friendly practices
- Cost-effective solutions
- Local climate adaptation
- Market opportunities
- Risk mitigation strategies

Format the response in clear, hierarchical bullet points with specific, actionable recommendations.
Use emojis to highlight key points (🌱 for sustainability, 🐛 for pest management, 💧 for water, etc.).
"""

MARKET_PROMPT_TEMPLATE = """
As a market analyst, analyze the following market scenario for {crop} in {location}:

Market Metrics:
- Average Market Price: ${metrics['avg_price']:.2f} per ton
- Average Demand Index: {metrics['avg_demand']:.2f}
- Average Supply Index: {metrics['avg_supply']:.2f}
- Average Competitor Price: ${metrics['avg_competitor_price']:.2f} per ton
- Average Weather Impact Score: {metrics['avg_weather_impact']:.2f}
- Trending Season: {metrics['trending_season']}
- Consumer Trend Index: {metrics['consumer_trend']:.2f}

Please provide insights focusing on:
1. Current market conditions and trends
2. Price competitiveness and profitability
3. Seasonal opportunities and risks
4. Demand-supply dynamics
5. Weather impact on market conditions
6. Consumer behavior and preferences

Format your response in clear sections with actionable recommendations.
"""

SUSTAINABILITY_PROMPT_TEMPLATE = """
You are a sustainability evaluator.
Input: {input}
Goal: Calculate expected carbon footprint, water usage, and environmental impact for chosen crop.
"""

VOICE_PROMPT_TEMPLATE = """
You are an assistant answering a voice-based query from a farmer.
Input: {input}
Goal: Understand natural language and forward it to the appropriate agent.
"""

