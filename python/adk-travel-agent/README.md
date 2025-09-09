# Okahu agent demo with Google Agent Development Kit
This repo includes a demo agent application built using Google Agent Development Kit (ADK).
This is a travel agent app that handles mock flight and hotel booking. It forces a low token usage due to which the agent's response is not half baked. The demo shows how you can use Monocle's tracing and MCP to find the root cause of the problem.

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
2. Open `adk-travel-agent.py` 
3. Replace <GOOGLE-API-KEY> with the value of Google API key
4. Right click on the file. It will pop up a list of menu options.
  - Select `Monocle` -->  `Run Python with Monocle`
5. The application will prompt you for a travel booking task. You can enter something like `Book a flight from San Francisco to Mumbai for 26th Nov 2025. Book a two queen room at Marriot Intercontinental at Juhu, Mumbai for 27th Nov 2025 for 4 nights.`
6. Follow these [steps](../../README.md#get-trace-summary-using-github-copilot-and-monocle-mcp) to review trace summary
