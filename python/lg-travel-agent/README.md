# Okahu agent demo with OpenAI + Langgraph
This repo includes a demo agent application built using OpenAI & Langgraph.
This is a travel agent app that handles mock flight and hotel booking. There's a supervisor agent that coordinates task with multiple agents that handle individual tasks like flight booking or hotel booking. Each agent has (mock) tools to execute these of the task. The weather agent uses an external tool hosted by an MCP server.
It forces a limit on max output token. This forces agent's response inaccurate for larger questions. The demo shows how you can use Monocle's tracing and MCP to find the root cause of the problem.

## Pre-requisting
- Follow the steps in top level [README](../../README.md) to setup environment running this example
- An OpenAI subscription and an API key to [OpenAI developer platform](https://platform.openai.com/overview)

## Prepare python env for application run
- Open a shell/terminal window
- Goto root folder of repository
- Activate virtual environment
  - Mac/Linux
  ```. ./.env/bin/activate```
  - Windows
  ```.env\scripts\activate```
- Install python dependencies
  - Mac or Linux
    - Install python dependencies: ```pip install -r ./python/adk-travel-agent/requirement.txt```
  - Windows
    - Install python dependencies: ```pip install -r .\python\adk-travel-agent\requirement.txt```

## Set API key in the demo app
- Edit lg-travel-agent.py and set the API key as follows:
  - Replace <OPENAI-API-KEY> with the value of OpenAI API key

## Run the app with Monocle instrumention in VS code
This application is an travel agent app that mocks travel related tasks like flight booking, hotel booking and checking weather in a city.
It's is a python program using Langgraph Agent framework. 
The app uses OpenAI gpt-4o model for inference.

1. Start VS Code and open the root repository folder
2. Open a new terminal windows in VS code
3. Start the mock weather MCP server in the new terminal window
  ```cd python/lg-travel-agent```
  ```python weather-mcp-server.py > mcp.out 2>&1 &```
4. Verify mcp server is running
  ```cat mcp.out```
  The above command prints content of mpc.out file which should show a message `Application startup complete`
5. Open `lg-travel-agent.py`
6. Replace <OPENAI-API-KEY> with the value of OpenAI API key
7. Right click on the file. It will pop up a list of menu options.
  - Select `Monocle` -->  `Run Python with Monocle`
8. The application will be launched in a new terminal window and it'll prompt you for a travel booking task.
  - A simple single task provides an accurate response `How's the weather going to be in Mumbai next week` 
  - A larger, more complex prompt results into inaccurate response `Book a flight from SFO to BOM next week. Book Marriot hotel in central mumbai. Also how't the weather going to be in Mumbai next week?`
9. Follow these [steps](../../README.md#get-trace-summary-using-github-copilot-and-monocle-mcp) to analyze the trace using Copilot and Monocle MCP. It'll illustrate how Monocle trace captures the details of the agentic execution and the how to determine the root cause of the problematic agent behavior.


