"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# Load activities from a JSON file
import json

activities_file = current_dir / "activities.json"
if activities_file.exists():
    with open(activities_file, "r") as f:
        activities = json.load(f)
else:
    activities = {}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    # Reload activities from the JSON file each time to ensure latest data
    activities_file = current_dir / "activities.json"
    if activities_file.exists():
        with open(activities_file, "r") as f:
            current_activities = json.load(f)
    else:
        current_activities = {}
    return current_activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Reload activities from the JSON file to ensure latest data
    activities_file = current_dir / "activities.json"
    if activities_file.exists():
        with open(activities_file, "r") as f:
            activities = json.load(f)
    else:
        activities = {}

    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up for this activity")

    # Add student
    activity["participants"].append(email)

    # Save updated activities back to the JSON file
    with open(activities_file, "w") as f:
        json.dump(activities, f, indent=2)

    return {"message": f"Signed up {email} for {activity_name}"}
