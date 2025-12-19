from asyncio import sleep
import os
import sys
import pytest 
import logging
from dotenv import load_dotenv

from adk_travel_agent import root_agent
from monocle_test_tools import TestCase, MonocleValidator



OKAHU_API_KEY = os.environ.get('OKAHU_API_KEY')
logging.basicConfig(level=logging.WARN)
load_dotenv()

agent_test_cases:list[TestCase] = [
    {
        "test_input": ["Book a flight from San Francisco to Mumbai for 26th March 2026. Book a two queen room at Marriot Intercontinental at Central Mumbai for 27th March 2026 for 4 nights."],
        "test_output": "A flight from San Francisco to Mumbai has been booked, along with a four night stay in a two queen room at the Marriot Intercontinental in Central Mumbai, starting March 27th, 2026.",
        "comparer": "similarity",
    },
    {
        "test_input": ["Book a flight from San Francisco to Mumbai for 26th April 2026. Book a two queen room at Marriot Intercontinental at Central Mumbai for 27th April 2026 for 4 nights."],
        "test_spans": [
            {
                "span_type": "agentic.turn",
                "output": "A flight from San Francisco to Mumbai has been booked, along with a four-night stay in a two queen room at the Marriot Intercontinental in Central Mumbai, starting April 27th, 2026.",
                "comparer": "similarity",
            },
            {
            "span_type": "agentic.invocation",
            "entities": [
                {"type": "agent", "name": "adk_supervisor_agent"}
                ]
            },
            {
            "span_type": "agentic.invocation",
            "entities": [
                {"type": "agent", "name": "adk_flight_booking_agent"}
                ]
            },
            {
                "span_type": "agentic.tool.invocation",
                "entities": [
                    {"type": "tool", "name": "adk_book_flight"},
                    {"type": "agent", "name": "adk_flight_booking_agent"}
                ]
            },
            {
            "span_type": "agentic.invocation",
            "entities": [
                {"type": "agent", "name": "adk_hotel_booking_agent"}
                ]
            },
            {
                "span_type": "agentic.tool.invocation",
                "entities": [
                    {"type": "tool", "name": "adk_book_hotel"},
                     {"type": "agent", "name": "adk_hotel_booking_agent"}
                ]
            },
            {
            "span_type": "agentic.invocation",
            "entities": [
                {"type": "agent", "name": "adk_trip_summary_agent"}
                ]
            }
        ]
    },
    {
        "test_input": ["Book a flight from San Francisco to Mumbai for 26th April 2026. Book a two queen room at Marriot Intercontinental at Central Mumbai for 27th April 2026 for 4 nights."],
        "test_spans": [
            {
                "span_type": "agentic.turn",
                # "output": "A flight from San Francisco to Mumbai has been booked, along with a four-night stay in a two queen room at the Marriot Intercontinental in Central Mumbai, starting April 27th, 2026.",
                "comparer": "similarity",
            },
            {
            "span_type": "agentic.invocation",
            "entities": [
                {"type": "agent", "name": "adk_supervisor_agent"}
                ]
            },
            {
            "span_type": "agentic.invocation",
            "entities": [
                {"type": "agent", "name": "adk_flight_booking_agent"}
                ],
            # "output": "Your flight from San Francisco to Mumbai on 26th April 2026 has been booked.",
            "comparer": "similarity"
            },
            {
                "span_type": "agentic.tool.invocation",
                "entities": [
                    {"type": "tool", "name": "adk_book_flight"},
                    {"type": "agent", "name": "adk_flight_booking_agent"}
                ],
                # "output": "{'status': 'success', 'message': 'Flight booked from San Francisco to Mumbai.'}",
                "expect_errors": False,
            },
            {
            "span_type": "agentic.invocation",
            "entities": [
                {"type": "agent", "name": "adk_hotel_booking_agent"}
                ],
            # "output": "Your stay at Marriot Intercontinental in Mumbai has been booked for 4 nights, starting from 27th April 2026.",
            "comparer": "similarity"
            },
            {
                "span_type": "agentic.tool.invocation",
                "entities": [
                    {"type": "tool", "name": "adk_book_hotel"},
                     {"type": "agent", "name": "adk_hotel_booking_agent"}
                ],
                # "output": "{'status': 'success', 'message': 'Successfully booked a stay at Marriot Intercontinental in Mumbai.'}",
                "comparer": "similarity",
            },
            {
            "span_type": "agentic.invocation",
            "entities": [
                {"type": "agent", "name": "adk_trip_summary_agent"}
                ],
            # "output": "Your flight from San Francisco to Mumbai on April 26th, 2026, and a 4-night stay at the Marriot Intercontinental in Mumbai starting April 27th, 2026, have been successfully booked",
            "comparer": "similarity"
            }
        ]
    },
    {
        "test_input": ["Book a flight from San Francisco to Mumbai for 26th April 2026. Book a two queen room at Marriot Intercontinental at Central Mumbai for 27th April 2026 for 4 nights."],
        "test_spans": [
            {
                "span_type": "agentic.turn",
                # "output": "A flight from San Francisco to Mumbai has been booked, along with a four-night stay in a two queen room at the Marriot Intercontinental in Central Mumbai, starting April 27th, 2026.",
                "comparer": "similarity",
            },
            {
                "span_type": "agentic.tool.invocation",
                "entities": [
                    {"type": "tool", "name": "adk_book_flight"},
                    {"type": "agent", "name": "adk_flight_booking_agent"}
                ],
                # "input": "{\"to_airport\": \"Mumbai\", \"date\": \"26th April 2026\", \"from_airport\": \"San Francisco\"}",
                # "output": "{'status': 'success', 'message': 'Flight booked from San Francisco to Mumbai.'}",
                "expect_errors": False,
            },
            {
                "span_type": "agentic.tool.invocation",
                "entities": [
                    {"type": "tool", "name": "adk_book_hotel"},
                     {"type": "agent", "name": "adk_hotel_booking_agent"}
                ],
                # "input": "{\"hotel_name\": \"Marriot Intercontinental\", \"city\": \"Central Mumbai\", \"check_in_date\": \"27th April 2026\", \"duration\": 4}",
                # "output": "{'status': 'success', 'message': 'Successfully booked a stay at Marriot Intercontinental in Central Mumbai.'}",
                "comparer": "similarity",
            }
        ]
    },
    
    {
        "test_input": ["Book a flight from San Francisco to Mumbai for 26th March 2026. Book a two queen room at Marriot Intercontinental at Juhu, Mumbai for 27th March 2026 for 4 nights."],
        "test_spans": [
            {
            "span_type": "agentic.turn",
            "eval":
                {
                "eval": "bert_score",
                "args" : [
                    "input", "output"
                ],
                "expected_result": {"Precision": 0.5, "Recall": 0.5, "F1": 0.5},
                "comparer": "metric"
                }
            }
        ]
    },
    {
        "test_input": ["Book a flight from San Francisco to Mumbai for 26th March 2026."],
        "mock_tools": [
            {
                "name": "adk_book_flight",
                "type": "tool.adk",
                "response": {
                    "status": "success",
                    "message": "Flight booked from {{from_airport}} to {{to_airport}}."
                }
            }
        ],
        "test_spans": [
            {
                "span_type": "agentic.tool.invocation",
                "entities": [
                    {"type": "tool", "name": "adk_book_flight"} 
                ],
                "output": "{'status': 'success', 'message': 'Flight booked from San Francisco to Mumbai.'}",
                "comparer": "similarity",
            }
        ]
    },
]

@MonocleValidator().monocle_testcase(agent_test_cases)
async def test_run_agents(my_test_case: TestCase):
   await MonocleValidator().test_agent_async(root_agent, "google_adk", my_test_case)
   await sleep(2) # Ensure all telemetry is flushed

if __name__ == "__main__":
    pytest.main([__file__]) 