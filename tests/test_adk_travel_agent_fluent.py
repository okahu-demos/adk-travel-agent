from asyncio import sleep
import pytest

from monocle_test_tools import TraceAssertion
from adk_travel_agent import root_agent

@pytest.mark.asyncio
async def test_tool_invocation(monocle_trace_asserter):
    await monocle_trace_asserter.run_agent_async(root_agent, "google_adk", 
                        "Book a flight from San Francisco to Mumbai for 26th April 2026. Book a two queen room at Marriot Intercontinental at Central Mumbai for 27th April 2026 for 4 nights.")
    
    monocle_trace_asserter.called_tool("adk_book_flight","adk_flight_booking_agent") \
        .contains_input("Mumbai").contains_input("San Francisco").contains_input("26th April 2026") \
        .contains_output("San Francisco to Mumbai").contains_output("success")
    
    monocle_trace_asserter.called_tool("adk_book_hotel","adk_hotel_booking_agent") \
        .contains_input("\"city\": \"Central Mumbai\",").contains_input("27th April 2026").contains_input("2Marriot Intercontinental") \
        .contains_output("Successfully booked a stay at Marriot Intercontinental in Mumbai").contains_output("success")


@pytest.mark.asyncio
async def test_agent_invocation(monocle_trace_asserter):
    await monocle_trace_asserter.run_agent_async(root_agent, "google_adk",
                        "Book a flight from San Francisco to Mumbai for 28th April 2026. Book a two queen room at Marriot Intercontinental at Central Mumbai for 29th April 2026 for 4 nights.")
    
    monocle_trace_asserter.called_agent("adk_flight_booking_agent") \
        .contains_input("Book a flight from San Francisco to Mumbai for 28th April 2026. Book a two queen room at Marriot Intercontinental at Central Mumbai for 29th April 2026 for 4 nights.") \
        .contains_output("booked a flight from San Francisco to Mumbai")
    
    monocle_trace_asserter.called_agent("adk_hotel_booking_agent") \
        .contains_input("Book a flight from San Francisco to Mumbai for 28th April 2026. Book a two queen room at Marriot Intercontinental at Central Mumbai for 29th April 2026 for 4 nights.") \
        .contains_output("booked a two queen room at Marriot Intercontinental at Central Mumbai")
    
    monocle_trace_asserter.called_agent("adk_trip_summary_agent") \
        .contains_input("Book a flight from San Francisco to Mumbai for 28th April 2026. Book a two queen room at Marriot Intercontinental at Central Mumbai for 29th April 2026 for 4 nights.") \
        .contains_output("booked from San Francisco to Mumbai ") \
        .contains_output("two queen room at Marriot Intercontinental at Central Mumbai")

if __name__ == "__main__":
    pytest.main([__file__]) 