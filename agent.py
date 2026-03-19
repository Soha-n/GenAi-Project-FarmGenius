from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from tools import (
    crop_selection,
    soil_health,
    weather_guidance,
    pest_disease_control,
    fertilizer_irrigation,
    market_price,
)

llm = ChatOllama(model="llama3.1", temperature=0.7)

tools = [
    crop_selection,
    soil_health,
    weather_guidance,
    pest_disease_control,
    fertilizer_irrigation,
    market_price,
]

prompt = """
You are an expert farming assistant AI. You have access to specialized tools for different farming objectives:

- crop_selection: Suggests suitable crops based on location, soil type, and climate
- soil_health: Analyzes soil health parameters and suggests improvements
- weather_guidance: Provides weather information and farming guidance
- pest_disease_control: Suggests control methods for pests and diseases
- fertilizer_irrigation: Recommends fertilizers and irrigation practices
- market_price: Provides market price information and trends

When a user asks about farming topics, use the appropriate tool(s) to gather information and provide comprehensive, actionable advice.

Always structure your responses clearly, using bullet points or numbered lists where appropriate. Be concise but informative.

If the query doesn't match any specific tool, use your general knowledge to assist.

"""

agent = create_agent(
    model = llm,
     tools =  tools,
      system_prompt= prompt)

agent_executor = agent
