import ollama
from typing import Dict, Any
from database.query_interface import get_sustainability_metrics
from agents.research_agent import ResearchAgent

class FarmerAdvisor:
    def __init__(self):
        self.models = {
            'sustainability': 'phi',  # Using phi for sustainability analysis
            'pest_management': 'tinyllama',  # Using tinyllama for pest management
            'resource_optimization': 'gemma',  # Using gemma for resource optimization
        }
        self.research_agent = ResearchAgent()
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

    def get_farm_advice(
        self,
        location: str,
        crop: str,
        soil_type: str,
        season: str = '',
        water_availability: str = '',
        previous_crop: str = '',
        pest_issues: str = ''
    ) -> Dict[str, Any]:
        """Get comprehensive farming advice using available models"""
        try:
            # Get sustainability metrics
            metrics = get_sustainability_metrics(crop, location)
            
            # Get research findings
            research_data = self.research_agent.get_sustainable_practices(crop, location)
            
            # Get advice from different models
            sustainability_advice = self._get_sustainability_advice(
                location, crop, soil_type, metrics, research_data
            )
            
            pest_management_advice = self._get_pest_management_advice(
                crop, pest_issues, research_data
            )
            
            resource_advice = self._get_resource_optimization_advice(
                location, crop, water_availability, metrics
            )
            
            # Combine all advice
            combined_advice = self._combine_advice(
                sustainability_advice,
                pest_management_advice,
                resource_advice
            )
            
            return {
                "advice": combined_advice,
                "metrics": metrics,
                "research_sources": [r['source'] for r in research_data]
            }
            
        except Exception as e:
            print(f"Error in get_farm_advice: {e}")
            return {
                "error": str(e),
                "metrics": None
            }

    def _get_sustainability_advice(
        self,
        location: str,
        crop: str,
        soil_type: str,
        metrics: Dict[str, float],
        research_data: list
    ) -> str:
        """Get sustainability advice from Phi-2 model"""
        prompt = f"""
        As a sustainable farming expert, provide concise and actionable advice for {crop} cultivation in {location} with {soil_type} soil.

        Current Metrics:
        - Sustainability Score: {metrics.get('sustainability_score', 'N/A')}
        - Fertilizer Usage: {metrics.get('fertilizer_usage', 'N/A')} kg/ha
        - Pesticide Usage: {metrics.get('pesticide_usage', 'N/A')} kg/ha
        - Crop Yield: {metrics.get('crop_yield', 'N/A')} tons/ha
        
        Research Findings:
        {self._format_research_data(research_data)}
        
        Provide advice focusing on:
        1. Sustainable farming practices
        2. Soil health improvement
        3. Resource optimization
        4. Environmental impact reduction

        Format the response in clear, concise bullet points with specific, actionable recommendations.
        """
        
        response = ollama.chat(
            model=self.models['sustainability'],
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a sustainable farming expert specializing in eco-friendly agricultural practices. Provide concise, actionable advice.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )
        
        return response['message']['content']

    def _get_pest_management_advice(
        self,
        crop: str,
        pest_issues: str,
        research_data: list
    ) -> str:
        """Get pest management advice from TinyLlama model"""
        prompt = f"""
        Provide concise pest management advice for {crop} cultivation.
        
        Known Pest Issues: {pest_issues or 'None specified'}
        
        Research Findings:
        {self._format_research_data(research_data)}
        
        Focus on:
        1. Integrated Pest Management (IPM) strategies
        2. Natural pest control methods
        3. Preventive measures
        4. Treatment options

        Format the response in clear, concise bullet points with specific, actionable recommendations.
        """
        
        response = ollama.chat(
            model=self.models['pest_management'],
            messages=[
                {
                    'role': 'system',
                    'content': 'You are an expert in agricultural pest management and control. Provide concise, actionable advice.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )
        
        return response['message']['content']

    def _get_resource_optimization_advice(
        self,
        location: str,
        crop: str,
        water_availability: str,
        metrics: Dict[str, float]
    ) -> str:
        """Get resource optimization advice from Gemma model"""
        prompt = f"""
        Provide concise resource optimization advice for {crop} cultivation in {location}.
        
        Water Availability: {water_availability}
        Current Metrics:
        - Water Usage: {metrics.get('water_usage', 'N/A')} liters/ha
        - Energy Consumption: {metrics.get('energy_usage', 'N/A')} kWh/ha
        - Resource Efficiency Score: {metrics.get('resource_efficiency', 'N/A')}
        
        Focus on:
        1. Water conservation techniques
        2. Energy efficiency
        3. Resource allocation
        4. Cost optimization

        Format the response in clear, concise bullet points with specific, actionable recommendations.
        """
        
        response = ollama.chat(
            model=self.models['resource_optimization'],
            messages=[
                {
                    'role': 'system',
                    'content': 'You are an expert in agricultural resource optimization and efficiency. Provide concise, actionable advice.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )
        
        return response['message']['content']

    def _format_research_data(self, research_data: list) -> str:
        """Format research data for prompts"""
        if not research_data:
            return "No recent research findings available."
        
        return "\n".join([
            f"- {item['title']}: {item['content'][:200]}..."
            for item in research_data[:3]  # Use top 3 most relevant findings
        ])

    def _combine_advice(self, sustainability: str, pest: str, resource: str) -> str:
        """Combine advice from different models into a comprehensive guide"""
        return f"""
        🌱 Comprehensive Farming Advice for Potato Cultivation in Haryana 🌱

        📊 Overview
        • Location: Haryana, India
        • Crop: Potato
        • Soil Type: Sandy
        • Season: Autumn
        • Water Availability: High

        1. 🌿 Sustainable Farming Practices
        {self._format_section(sustainability)}

        2. 🐛 Pest Management
        {self._format_section(pest)}

        3. 💧 Resource Optimization
        {self._format_section(resource)}

        📅 Implementation Timeline
        • Week 1: Initial setup and soil preparation
        • Month 1-3: Implementation of core practices
        • Month 4-6: Monitoring and adjustments
        • Month 7-12: Scaling and optimization

        📝 Key Recommendations
        • Prioritize sustainable practices that align with your farm's conditions
        • Implement pest management strategies gradually
        • Monitor resource usage and adjust practices accordingly
        • Keep detailed records of implemented changes and outcomes

        🔍 Monitoring & Evaluation
        • Weekly: Soil moisture and plant health checks
        • Monthly: Resource usage and pest monitoring
        • Quarterly: Yield assessment and practice adjustments
        • Annually: Comprehensive sustainability review
        """

    def _format_section(self, content: str) -> str:
        """Format a section with proper indentation and bullet points"""
        # Split content into lines and format each line
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            if line.strip():
                # Add proper indentation and bullet points
                if line.startswith('•'):
                    formatted_lines.append(f"    {line}")
                elif line.startswith('-'):
                    formatted_lines.append(f"      {line}")
                else:
                    formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
