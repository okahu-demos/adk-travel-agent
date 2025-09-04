# Okahu agent demo with Google Agent Development Kit
This repo includes a demo agent application built using Google Agent Development Kit (ADK) that is pre-instrumented for observation with Okahu AI Observability cloud. 
You can fork this repo and run the app in Github Codespaces or laptop/desktop to get started quickly.

## Try Okahu with this Agentic app

To try this agent 
- Fork this repo and run in the Github Codespace
- Create python virtual envirmonment
```python -m venv .env```
- To run this on Mac 
  - Install python dependencies: ```pip install -r requirement.txt```
- To run this on Windows
  - Install python dependencies: ```pip install -r requirement.txt```

You'll need 
- An GCP subscription and an API key to [Gemini API](https://ai.google.dev/gemini-api/docs)
- An Okahu tenant and API key to [Okahu AI Observability Cloud](https://www.okahu.co)
  - Sign up for Okahu AI accout with your LinkedIn for Github ID
  - Once you login, nagivate to 'Settings' on the left navigation bar and click on 'Generate Okahu API Key'
  - Copy the API key generated and save. Note that you'll not be able to extract that API key after you navigate away from that page.

## Configure the demo environment
- Edit adk-travel-agent.py and set the API keys as follows:
  - Replace <GOOGLE-API-KEY> with the value of OpenAI API key
  - Replace <OKAHU-API-KEY> with the value of Okahu API key

## Run the travel agent app 
This application is an travel agent app that mocks travel related tasks like flight booking, hotel booking.
It's is a python program using Google Agent Development Kit. 
The app uses Gemini gemini-2.0-flash model for inference.

1. Run the pre-instrumented travel agent app with following command
   ```python adk-travel-agent.py```
   The application will prompt you for a travel booking task. You can enter something like `Book a flight from San Francisco to Mumbai for 26th Nov 2025. Book a two queen room at Marriot Intercontinental at Juhu, Mumbai for 27th Nov 2025 for 4 nights.`
   It should responds with successful booking of flight and hotel, as well as weather forcast.
