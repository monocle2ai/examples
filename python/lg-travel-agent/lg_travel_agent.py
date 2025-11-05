# Enable Monocle Tracing
from dotenv import load_dotenv

import asyncio
import os
import time
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from langchain_core.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient

import logging
logger = logging.getLogger(__name__)
DEFAULT_PORT = 8007
port = int(os.getenv("PORT", DEFAULT_PORT))
MAX_OUTPUT_TOKENS = 50
load_dotenv()
from monocle_apptrace import setup_monocle_telemetry
setup_monocle_telemetry(workflow_name = 'examples', monocle_exporters_list = 'file')

@tool("lg-tool_book_hotel", description="Book a hotel for a stay")
def book_hotel(hotel_name: str):
    """Book a hotel"""
    return f"Successfully booked a stay at {hotel_name}."

@tool("lg-tool_book_flight", description="Book a flight from one airport to another")
def book_flight(from_airport: str, to_airport: str):
    """Book a flight"""
    return f"Successfully booked a flight from {from_airport} to {to_airport}."

# Set up MCP client for monocle repo
async def get_mcp_tools():
    """Get tools from the monocle MCP server."""
    client = MultiServerMCPClient(
        {
            "weather": {
                "url": f"http://localhost:{port}/weather/mcp/",
                "transport": "streamable_http",
            }
        }
    )
    # get list of all tools from the MCP server and their descriptions
    tools = await client.get_tools()
    return tools

# Set up agents for travel booking
async def setup_agents():

    weather_tools = await get_mcp_tools()

    flight_assistant = create_react_agent(
        model="openai:gpt-4o",
        tools=[book_flight],
        prompt="You are a flight booking assistant",
        name="lg-agent-air_travel_assistant"
    )

    hotel_assistant = create_react_agent(
        model="openai:gpt-4o",
        tools=[book_hotel],
        prompt="You are a hotel booking assistant",
        name="lg-agent-lodging_assistant"
    )

    weather_agent = create_react_agent(
        model="openai:gpt-4o",
        tools=weather_tools,
        prompt="You are a weather information assistant. Please use the tool available to you for checking weather. Extract city name from the user query and pass it to the weather tool.",
        name="lg-agent-weather_assistant"
    )
    supervisor = create_supervisor(
        supervisor_name="lg-agent-travel_supervisor",
        agents=[flight_assistant, hotel_assistant, weather_agent],
        model=ChatOpenAI(model="gpt-4o", max_completion_tokens=MAX_OUTPUT_TOKENS),
        prompt=(
            "You manage a hotel booking assistant and a"
            "flight booking assistant. Assign work to them."
            "If the user asks for weather information, delegate to the weather assistant."
        )
    ).compile()

    return supervisor

# Run the agent with a user request
async def run_agent(request: str):
    supervisor = await setup_agents()
    chunk = await supervisor.ainvoke(
        input={
            "messages": [
                {
                    "role": "user",
                    "content": request
            }
        ]
    })
    print(chunk["messages"][-1].content)
    return chunk["messages"][-1].content

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    request = input("\nI am a travel booking agent. How can I assist you with your travel plans? (You can ask me to book flights, hotels, or check the weather at any location.): ")
    asyncio.run(run_agent(request))
