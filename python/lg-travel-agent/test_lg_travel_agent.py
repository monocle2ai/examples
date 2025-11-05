import os
import pytest 
import logging
from monocle_test_tools import MonocleValidator, TestCase
from lg_travel_agent import run_agent

logging.basicConfig(level=logging.WARN)

agent_test_cases:list[TestCase] = [
    # {
    #     "test_input": ["How's the weather in Seattle?"],
    #     "test_output": "The current temperature in Seattle is 52°F",
    #     "comparer": "similarity",
    # },
    # {
    #     "test_input": ["Book a flight from SFO to BOM next week. Book Marriot hotel in central mumbai."],
    #     "test_spans": [
    #         {
    #         "span_type": "agentic.tool.invocation",
    #         "entities": [
    #             {"type": "tool", "name": "-lg-tool_book_flight"},
    #             {"type": "agent", "name": "-lg-agent-air_travel_assistant"}
    #         ],
    #     }
    #     ]
    # },
    # {
    #     "test_input": ["Book a flight from SFO to BOM next week. Book Marriot hotel in central mumbai."],
    #     "test_spans": [
    #         {
    #         "span_type": "agentic.invocation",
    #         "entities": [
    #             {"type": "agent", "name": "-lg-agent-travel_supervisor"}
    #         ],
    #         "expect_errors": True,
    #         }
    #     ]
    # }
    {
        "test_input": ["Book a flight from San Francisco to Mumbai for 26th Nov 2025."],
        # "mock_tools": [
        #     {
        #         "name": "-lg-tool_book_flight",
        #         "type": "tool.adk",
        #         "response": {
        #             "status": "success",
        #             "message": "Flight booked from {{from_airport}} to {{to_airport}}."
        #         }
        #     }
        # ],
        "test_spans": [
            {
                "span_type": "agentic.tool.invocation",
                "entities": [
                    {"type": "tool", "name": "-lg-tool_book_flight"},
                ],
                "output": "Successfully booked a flight from San Francisco to Mumbai.",
                "comparer": "similarity",
            }
        ]
    },
    ]

@MonocleValidator().monocle_testcase(agent_test_cases)
async def test_lg_agents(my_test_case: TestCase):
    await MonocleValidator().test_workflow_async(run_agent, my_test_case)

if __name__ == "__main__":
    pytest.main([__file__]) 