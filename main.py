from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()
app = FastAPI()
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")


# Config
USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"  # Toggle in .env
VEO_API_KEY = os.getenv("VEO3_API_KEY")
BASE_URL = "https://api.veo3api.ai/api/v1/veo"

@app.get("/", response_class=HTMLResponse)
def home():
    return open("index.html").read()

@app.post("/generate")
def generate_video(prompt: str = Form(...)):
    if USE_MOCK:
        print(f"MOCK MODE: Pretending to send prompt → {prompt}")
        return {"video_url": "/static/sample.mp4"}

    headers = {
        "Authorization": f"Bearer {VEO_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "model": "veo3",          
        "aspectRatio": "9:16",    
        "seconds": 5,
        "enableFallback": False
    }

    # Step 1: Start generation
    r = requests.post(f"{BASE_URL}/generate", json=payload, headers=headers)
    print("DEBUG API RESPONSE:", r.status_code, r.text)

    if r.status_code != 200:
        try:
            err_msg = r.json().get("message", r.text)
        except:
            err_msg = r.text
        return {"error": err_msg}

    data = r.json()
    task_id = data.get("data", {}).get("taskId")
    if not task_id:
        return {"error": f"API did not return taskId. Full response: {data}"}

    print(f"DEBUG: Got taskId = {task_id}")

    # Step 2: Poll until ready
    status_url = f"{BASE_URL}/status/{task_id}"
    start_time = time.time()

    while True:
        status_res = requests.get(status_url, headers=headers)
        status_data = status_res.json()
        print("DEBUG POLLING STATUS:", status_data)

        status_value = status_data.get("data", {}).get("status")
        video_url = status_data.get("data", {}).get("videoUrl")

        if status_value == "completed" and video_url:
            print(f"DEBUG: Video ready after {int(time.time() - start_time)}s")
            return {"video_url": video_url}
        elif status_value == "failed":
            fail_msg = status_data.get("data", {}).get("message", "unknown reason")
            return {"error": f"Video generation failed: {fail_msg}"}

        if time.time() - start_time > 300:
            return {"error": "Video generation timed out after 5 minutes"}

        time.sleep(5)
