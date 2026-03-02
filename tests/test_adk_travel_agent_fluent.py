from asyncio import sleep
import pytest

from monocle_test_tools import TraceAssertion
from adk_travel_agent import root_agent

@pytest.mark.asyncio
async def test_sentiment_bias_evaluation(monocle_trace_asserter):
    """v0: Basic sentiment, bias evaluation on trace - only specify eval name and expected value."""
    await monocle_trace_asserter.run_agent_async(root_agent, "google_adk",
                        "Book a flight from San Jose to Seattle for 27th Nov 2025.")
    # Fact is implicit (trace), only specify eval template name and expected value
    monocle_trace_asserter.with_evaluation("okahu").check_eval("sentiment", "positive")\
        .check_eval("bias", "unbiased")

@pytest.mark.asyncio
async def test_quality_evaluation(monocle_trace_asserter):
    """v0: Multiple evaluations on trace - frustration, hallucination, contextual_precision."""
    await monocle_trace_asserter.run_agent_async(root_agent, "google_adk",
                        "Please Book a flight from New York to Hamburg for 1st Dec 2025. Book a flight from Hamburg to Paris on January 1st. " \
                        "Then book a hotel room in Paris for 5th Jan 2026.")
    # You can chain multiple check_eval calls for different eval templates. 
    # The expected value is based on the eval template definition. 
    monocle_trace_asserter.with_evaluation("okahu").check_eval("frustration", "ok")\
        .check_eval("hallucination", "no_hallucination")
    # You only have to declare the evaluator once
    monocle_trace_asserter.check_eval("contextual_precision", "high_precision")


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
    # example error case: check_eval will return non_toxic. Test will fail as expected since we are checking for toxic. 
    # This is to demonstrate how to use check_eval for error cases as well.
    monocle_trace_asserter.with_evaluation("okahu").check_eval("toxicity", "toxic")


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