# Okahu agent demo with Google Agent Development Kit
This repo includes a demo agent application built using Google Agent Development Kit (ADK).
This is a travel agent app that handles mock flight and hotel booking. It forces a low token usage due to which the agent's response is not half baked. The demo shows how you can use Monocle's tracing and MCP to find the root cause of the problem.

## Pre-requisting
- Follow the steps in top level [README](../../README.md) to setup environment running this example
- You need a GCP subscription and an API key to [Gemini API](https://ai.google.dev/gemini-api/docs)

## Set API key in the demo app
- Edit adk-travel-agent.py and set the API keys as follows:
  - Replace <GOOGLE-API-KEY> with the value of OpenAI API key

## Run the app with Monocle instrumention in VS code
This application is a travel agent app that mocks travel related tasks like flight booking, hotel booking.
It's is a python program using Google Agent Development Kit. 
The app uses Gemini gemini-2.0-flash model for inference.

1. Open `adk-travel-agent.py` and follow these [steps](../../README.md#run-application-with-monocle-tracing-enabled) to enable Monocle instrumentation using Monocle VS Code plugin
2. The application will prompt you for a travel booking task. You can enter something like `Book a flight from San Francisco to Mumbai for 26th Nov 2025. Book a two queen room at Marriot Intercontinental at Juhu, Mumbai for 27th Nov 2025 for 4 nights.`
3. Follow these [steps](../../README.md#get-trace-summary-using-github-copilot-and-monocle-mcp) to review trace summary
