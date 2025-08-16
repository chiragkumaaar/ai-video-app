# AI Video Generator

A FastAPI + HTML app that generates short AI videos from text prompts using the Veo 3 API.
Supports mock mode (placeholder video) for quick testing without spending credits.

# Features

Enter a text prompt and generate a video in the browser

Mock mode: instant placeholder video (no credits used)

Real mode: integrates with Veo 3 API to generate real videos

Deployable to Render, Vercel, or Railway

# Folder Structure

ai-video-app/
│── main.py           # FastAPI backend
│── index.html        # frontend
│── requirements.txt  # Dependencies
│── .env              # API keys + config
│── static/
│    └── sample.mp4   # Placeholder video

# Setup

1. Clone repo and create venv

git clone https://github.com/yourusername/ai-video-app.git
cd ai-video-app
python -m venv venv
source venv/bin/activate

2. Install dependencies

pip install -r requirements.txt

3. Create .env file

USE_MOCK=true

VEO3_API_KEY=your_api_key_here

Run locally

uvicorn main:app --reload

# Deployment

Push repo to GitHub

On Render, create a new Web Service and connect the repo

Environment: Python 3.10+

Start command:

uvicorn main:app --host 0.0.0.0 --port 10000

Add environment variables in Render dashboard:

USE_MOCK=false
VEO3_API_KEY=your_api_key_here




# Mock vs Real Mode

Mock mode (USE_MOCK=true) #For Mock Case

Returns static/sample.mp4 instantly

Fast, free, no credits used

Real mode (USE_MOCK=false)

Calls Veo 3 API with prompt

Uses credits each run

Slower (20s–2min)


