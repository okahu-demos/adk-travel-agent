from asyncio import sleep
import pytest

from monocle_test_tools import TraceAssertion
from adk_travel_agent import root_agent

@pytest.mark.asyncio
async def test_tool_invocation1(monocle_trace_asserter):
    await monocle_trace_asserter.run_agent_async(root_agent, "google_adk", 
                        "Book a flight from San Francisco to Mumbai for 26th April 2026. Book a two queen room at Marriott Intercontinental at Central Mumbai for 27th April 2026 for 4 nights.")
    
    monocle_trace_asserter.called_tool("adk_book_flight","adk_flight_booking_agent") \
        .contains_input("Mumbai").contains_input("San Francisco").contains_input("26th April 2026") \
        .contains_output("San Francisco to Mumbai").contains_output("success")
    
    monocle_trace_asserter.called_tool("adk_book_hotel","adk_hotel_booking_agent") \
        .contains_input("Central Mumbai").contains_input("27th April 2026").contains_input("Marriott Intercontinental") \
        .contains_output("booked") \
        .contains_output("Successfully booked a stay at Marriott Intercontinental in Central Mumbai") \
        .contains_output("success")


@pytest.mark.asyncio
async def test_agent_invocation2(monocle_trace_asserter):
    await monocle_trace_asserter.run_agent_async(root_agent, "google_adk",
                        "Book a flight from San Francisco to Mumbai for 28th April 2026. Book a two queen room at Marriott Intercontinental at Mumbai for 29th April 2026 for 4 nights.")
    
    monocle_trace_asserter.called_agent("adk_flight_booking_agent") \
        .contains_input("Book a flight from San Francisco to Mumbai for 28th April 2026. Book a two queen room at Marriott Intercontinental at Mumbai for 29th April 2026 for 4 nights.") \
        .contains_output("flight from San Francisco to Mumbai") \
        .contains_output("28th April 2026") \
        .contains_output("booked")
    
    monocle_trace_asserter.called_agent("adk_hotel_booking_agent") \
        .contains_input("Book a flight from San Francisco to Mumbai for 28th April 2026. Book a two queen room at Marriott Intercontinental at Mumbai for 29th April 2026 for 4 nights.") \
        .contains_output("booked") \
        .contains_output("two queen room at Marriott Intercontinental") \
        .contains_output("Mumbai")
    
    monocle_trace_asserter.called_agent("adk_trip_summary_agent") \
        .contains_input("Book a flight from San Francisco to Mumbai for 28th April 2026. Book a two queen room at Marriott Intercontinental at Mumbai for 29th April 2026 for 4 nights.") \
        .contains_output("flight from San Francisco to Mumbai ") \
        .contains_output("28th April 2026") \
        .contains_output("two queen room at Marriott Intercontinental") \
        .contains_output("Mumbai") \
        .contains_output("29th April 2026")

@pytest.mark.asyncio
async def test_tool_invocation3(monocle_trace_asserter):
    await monocle_trace_asserter.run_agent_async(root_agent, "google_adk", 
                        "Book a flight from San Francisco to Mumbai for 26th April 2026. Book a two queen room at Marriott Intercontinental at Mumbai for 27th April 2026 for 4 nights.")
    
    monocle_trace_asserter.called_tool("adk_book_flight","adk_flight_booking_agent") \
        .contains_input("Mumbai").contains_input("San Francisco") \
        .contains_output("San Francisco to Mumbai").contains_output("success")
    
    monocle_trace_asserter.called_tool("adk_book_hotel","adk_hotel_booking_agent") \
        .contains_input("Mumbai").contains_input("Marriott Intercontinental") \
        .contains_output("booked") \
        .contains_output("Marriott Intercontinental") \
        .contains_output("Mumbai") \
        .contains_output("success")


@pytest.mark.asyncio
async def test_agent_invocation4(monocle_trace_asserter):
    await monocle_trace_asserter.run_agent_async(root_agent, "google_adk",
                        "Book a flight from San Francisco to Mumbai for 28th April 2026. Book a two queen room at Marriott Intercontinental at Mumbai for 29th April 2026 for 4 nights.")
    
    monocle_trace_asserter.called_agent("adk_flight_booking_agent") \
        .contains_input("Book a flight from San Francisco to Mumbai for 28th April 2026. Book a two queen room at Marriott Intercontinental at Mumbai for 29th April 2026 for 4 nights.") \
        .contains_output("San Francisco to Mumbai") \
        .contains_output("28").contains_output("April").contains_output("2026") \
        .contains_output("booked")
    
    monocle_trace_asserter.called_agent("adk_hotel_booking_agent") \
        .contains_input("Book a flight from San Francisco to Mumbai for 28th April 2026. Book a two queen room at Marriott Intercontinental at Mumbai for 29th April 2026 for 4 nights.") \
        .contains_output("booked") \
        .contains_output("Marriott Intercontinental") \
        .contains_output("Mumbai")
    
    monocle_trace_asserter.called_agent("adk_trip_summary_agent") \
        .contains_input("Book a flight from San Francisco to Mumbai for 28th April 2026. Book a two queen room at Marriott Intercontinental at Mumbai for 29th April 2026 for 4 nights.") \
        .contains_output("San Francisco to Mumbai") \
        .contains_output("28").contains_output("April").contains_output("2026") \
        .contains_output("Marriott Intercontinental") \
        .contains_output("Mumbai")
    
if __name__ == "__main__":
    pytest.main([__file__]) 