# Okahu agent demo with OpenAI + Langgraph
This repo includes a demo agent application built using OpenAI & Langgraph that is pre-instrumented for observation with Okahu AI Observability cloud. 
You can fork this repo and run the app in Github Codespaces or laptop/desktop to get started quickly.

## Pre-requisting
- Follow the steps in top level [README](../../README.md) to setup environment running this example
- An OpenAI subscription and an API key to [OpenAI developer platform](https://platform.openai.com/overview)

## Set API key in the demo app
- Edit lg-travel-agent.py and set the API key as follows:
  - Replace <OPENAI-API-KEY> with the value of OpenAI API key

## Run the app with Monocle instrumention in VS code
This application is an travel agent app that mocks travel related tasks like flight booking, hotel booking and checking weather in a city.
It's is a python program using Langgraph Agent framework. 
The app uses OpenAI gpt-4o model for inference.

1. Start the mock weather MCP server
  ```python weather-mcp-server.py > mcp.out 2>&1 &```
2. Verify mcp server is running
  ```cat mcp.out```
  The above command prints content of mpc.out file which should show a message `Application startup complete`
3. Open `lg-travel-agent.py` and follow these [steps](../../README.md#run-application-with-monocle-tracing-enabled) to enable Monocle instrumentation using Monocle VS Code plugin
   The application will prompt you for a travel booking task. You can enter something like `Book a flight from SFO to BOM next week. Book Marriot hotel in central mumbai. Also how't the weather going to be in Mumbai next week?`
4. Follow these [steps](../../README.md#get-trace-summary-using-github-copilot-and-monocle-mcp) to review trace summary


