from langchain.tools import tool
from langchain_ollama import ChatOllama

# Using Ollama with llama3.1 model
llm = ChatOllama(model="llama3.1", temperature=0.7)

@tool("crop_selection", description="Suggest suitable crops based on location, soil type, and climate. Input should be a string with location, soil_type, climate separated by commas.")
def crop_selection(input_str: str) -> str:
    try:
        location, soil_type, climate = input_str.split(',')
        prompt = f"Suggest 3-5 suitable crops for farming in {location.strip()} with {soil_type.strip()} soil type and {climate.strip()} climate. Provide brief reasons for each."
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"

@tool("soil_health", description="Analyze soil health based on pH, nitrogen, phosphorus, potassium levels. Input: pH, N, P, K separated by commas.")
def soil_health(input_str: str) -> str:
    try:
        pH, N, P, K = input_str.split(',')
        prompt = f"Analyze soil health with pH {pH.strip()}, Nitrogen {N.strip()}, Phosphorus {P.strip()}, Potassium {K.strip()}. Suggest improvements and maintenance tips."
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"

@tool("weather_guidance", description="Provide weather guidance for farming in a location. Input: location")
def weather_guidance(location: str) -> str:
    try:
        prompt = f"Provide current weather conditions and 7-day forecast guidance for farming activities in {location.strip()}. Include temperature, rainfall, humidity, and specific farming advice like planting, harvesting, or protection measures."
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"

@tool("pest_disease_control", description="Suggest pest and disease control methods for a specific crop and issue. Input: crop, pest_or_disease separated by comma.")
def pest_disease_control(input_str: str) -> str:
    try:
        crop, issue = input_str.split(',')
        prompt = f"For {crop.strip()} crop affected by {issue.strip()}, suggest organic and chemical control methods, preventive measures, and best practices."
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"

@tool("fertilizer_irrigation", description="Suggest fertilizers and irrigation schedules for a crop and soil type. Input: crop, soil_type separated by comma.")
def fertilizer_irrigation(input_str: str) -> str:
    try:
        crop, soil_type = input_str.split(',')
        prompt = f"For {crop.strip()} in {soil_type.strip()} soil, recommend appropriate fertilizers (types, amounts, timing), irrigation methods, frequency, and water management practices."
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"

@tool("market_price", description="Get current market price information and trends for a crop. Input: crop")
def market_price(crop: str) -> str:
    try:
        prompt = f"Provide current market prices for {crop.strip()} in major agricultural regions worldwide. Include average prices per unit, recent trends, factors affecting prices, and future outlook."
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"
