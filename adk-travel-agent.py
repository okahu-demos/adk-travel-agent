import datetime
import asyncio
import logging
import os
from zoneinfo import ZoneInfo

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from monocle_apptrace import setup_monocle_telemetry
setup_monocle_telemetry(workflow_name = 'adk-travel-agent', monocle_exporters_list = 'file,okahu')

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"
MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS", "1000"))
# Set env model as gemini-2.5-flash-lite by default
GOOGLE_GENAI_MODEL = os.getenv("GOOGLE_GENAI_MODEL", "gemini-2.5-flash-lite")

def adk_book_flight(from_airport: str, to_airport: str, date: str = None) -> dict:
    """Books a flight from one airport to another.

    Args:
        from_airport (str): The airport from which the flight departs.
        to_airport (str): The airport to which the flight arrives.
        date (str): The date of the flight.

    Returns:
        dict: status and message.
    """
    return {
        "status": "success",
        "message": f"Flight booked from {from_airport} to {to_airport}" + (f" on {date}" if date else "") + "."
    }

def adk_book_hotel(hotel_name: str, city: str, check_in_date: str = None, duration: int = 1) -> dict:
    """Books a hotel for a stay.

    Args:
        hotel_name (str): The name of the hotel to book.
        city (str): The city where the hotel is located.
        check_in_date (str): The check-in date for the hotel stay.
        duration (int): The duration of the hotel stay in nights.

    Returns:
        dict: status and message.
    """
    return {
        "status": "success",
        "message": f"Successfully booked a stay at {hotel_name} in {city}" + (f" for {duration} night(s)" if duration > 1 else "") + (f" starting {check_in_date}" if check_in_date else "") + "."
    }

contentConfig: types.GenerateContentConfig = types.GenerateContentConfig(max_output_tokens=MAX_OUTPUT_TOKENS)
flight_booking_agent = LlmAgent(
    name="adk_flight_booking_agent",
    model=GOOGLE_GENAI_MODEL,
    description= "Agent to book flights based on user queries.",
    instruction= "You are a helpful agent who can assist users in booking flights. When booking flights, always ask for the departure airport if not provided. Parse user requests carefully to extract flight details. If a user mentions 'Flight Hotel', clarify whether they want flight booking, hotel booking, or both services.",
    generate_content_config=contentConfig,
    tools=[adk_book_flight]  # Define flight booking tools here
)

hotel_booking_agent = LlmAgent(
    name="adk_hotel_booking_agent",
    model=GOOGLE_GENAI_MODEL,
    description= "Agent to book hotels based on user queries.",
    instruction= "You are a helpful agent who can assist users in booking hotels. If you are asked about hotel bookings, provide the relevant information. If not, then just stay silent. IMPORTANT: When users mention 'Flight Hotel', ask for clarification: Do they mean a hotel literally named 'Flight Hotel', a hotel near the airport, or are they requesting both flight and hotel services? Only proceed with booking after confirming the hotel name. NOTE: Marriott is only available on odd dates. Otherwise Hilton is the primary option unless user states specific hotel criteria and you can go ahead and book that instead.",
    generate_content_config=contentConfig,
    tools=[adk_book_hotel]  # Define hotel booking tools here
)

trip_summary_agent = LlmAgent(
    name="adk_trip_summary_agent",
    model=GOOGLE_GENAI_MODEL,
    description= "Summarize the travel details from hotel bookings and flight bookings agents.",
    instruction= "Summarize the travel details from hotel bookings and flight bookings agents.",
    generate_content_config=contentConfig,
    output_key="booking_summary"
)

root_agent = SequentialAgent(
    name="adk_supervisor_agent",
    description=
        """
            You are the supervisor agent that coordinates the flight booking and hotel booking.
            You must provide a consolidated summary back to the full coordination of the user's request.
        """
    ,
    sub_agents=[flight_booking_agent, hotel_booking_agent, trip_summary_agent],
)

session_service = InMemorySessionService()
APP_NAME = "streaming_app"
USER_ID = "user_123"
SESSION_ID = "session_456"

runner = Runner(
    agent=root_agent,  # Assume this is defined
    app_name=APP_NAME,
    session_service=session_service
)

async def run_agent(test_message: str):
    session = await session_service.create_session(
        app_name=APP_NAME, 
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    session.model_config
    content = types.Content(role='user', parts=[types.Part(text=test_message)])
    response = None
    # Process events as they arrive using async for\
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=content
    ):
        # For final response
        if event.is_final_response():
            response = event.content

    print(response.parts[0].text)  # Print the last response text

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)

    user_request = input("\nI am a travel booking agent. How can I assist you with your travel plans? ")
    asyncio.run(run_agent(user_request))