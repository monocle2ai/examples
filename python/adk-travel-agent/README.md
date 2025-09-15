# Okahu agent demo with Google Agent Development Kit
This repo includes a demo agent application built using Google Agent Development Kit (ADK).
This is a travel agent app that handles mock flight and hotel booking. There's a root agent that coordinates task with multiple agents that handle individual tasks like flight booking or hotel booking. Each agent has (mock) tools to execute these of the task. To simulate problems in real world scenarios, this app has set a limit on max output token. This results int problems when agent is asked to perform large/complext tasks.


## Pre-requisting
- Follow the steps in top level [README](../../README.md) to setup environment running this example
- You need a GCP subscription and an API key to [Gemini API](https://ai.google.dev/gemini-api/docs)

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

## Run the app with Monocle instrumention in VS code
This application is a travel agent app that mocks travel related tasks like flight booking, hotel booking.
It's is a python program using Google Agent Development Kit. 
The app uses Gemini gemini-2.0-flash model for inference.

1. Start VS Code and open the root repository folder
2. copy `env.template` to `.env` under the root repository folder
3. Open `.env` set value for <GOOGLE-API-KEY> to your Google API key
4. Right click on the file. It will pop up a list of menu options.
  - Select `Monocle` -->  `Run Python with Monocle`
5. The application will be launched in a new terminal window and it'll prompt you for a travel booking task.
  - A simple task will generate accurate response `Book a flight from SFO to JFK for tomorrow.`
  - A larger, more complex prompt results into inaccurate response `Book a flight from San Francisco to Mumbai for 26th Nov 2025. Book a two queen room at Marriot Intercontinental at Juhu, Mumbai for 27th Nov 2025 for 4 nights.`
6. Follow these [steps](../../README.md#get-trace-summary-using-github-copilot-and-monocle-mcp) to analyze the trace using Copilot and Monocle MCP. It'll illustrate how Monocle trace captures the details of the agentic execution and the how to determine the root cause of the problematic agent behavior.
