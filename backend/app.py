# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.farmer_advisor import FarmerAdvisor
from agents.market_researcher import MarketResearcher
from agents.sustainability_metrics import evaluate_sustainability

app = Flask(__name__)
CORS(app)

# Initialize agents
farmer_advisor = FarmerAdvisor()
market_researcher = MarketResearcher()

@app.route('/query', methods=['POST'])
def query_handler():
    user_input = request.json.get("input")
    if not user_input:
        return jsonify({"error": "Missing input parameter"})
    
    try:
        # Parse the input string into a structured format
        input_parts = user_input.split(', ')
        input_dict = {}
        for part in input_parts:
            key, value = part.split(': ', 1)
            input_dict[key.lower().replace(' ', '_')] = value
        
        # Extract required parameters
        location = input_dict.get('location')
        crop = input_dict.get('crop')
        soil_type = input_dict.get('soil_type')
        
        if not all([location, crop, soil_type]):
            return jsonify({"error": "Missing required parameters: location, crop, and soil_type"})
        
        # Get additional parameters
        season = input_dict.get('season', '')
        water_availability = input_dict.get('water_availability', '')
        previous_crop = input_dict.get('previous_crop', '')
        pest_issues = input_dict.get('pest_issues', '')
        
        # Get the advice
        result = farmer_advisor.get_farm_advice(
            location=location,
            crop=crop,
            soil_type=soil_type,
            season=season,
            water_availability=water_availability,
            previous_crop=previous_crop,
            pest_issues=pest_issues
        )

        if "error" in result:
            return jsonify({"error": result["error"]})

        # Ensure all required fields are present
        response = {
            "advice": result.get("advice", ""),
            "metrics": result.get("metrics", {}),
            "research_sources": result.get("research_sources", [])
        }

        print("Sending response:", response)  # Debug log
        return jsonify(response)

    except Exception as e:
        print("Error in query_handler:", str(e))  # Debug log
        return jsonify({"error": str(e)})

@app.route('/market', methods=['POST'])
def market_handler():
    region = request.json.get("region")
    crop = request.json.get("crop")
    return jsonify({"market_info": market_researcher.get_market_trends(region, crop)})

@app.route('/sustainability', methods=['POST'])
def sustainability_handler():
    crop = request.json.get("crop")
    soil = request.json.get("soil")
    return jsonify({"sustainability": evaluate_sustainability(crop, soil)})

if __name__ == "__main__":
    app.run(debug=True)
