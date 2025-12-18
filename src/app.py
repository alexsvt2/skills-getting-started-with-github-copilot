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

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball league for students of all skill levels",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Soccer Club": {
        "description": "Outdoor soccer practice and friendly matches",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 22,
        "participants": ["lucas@mergington.edu", "isabella@mergington.edu"]
    },
    "Drama Club": {
        "description": "Script writing, acting, and theater production",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["amelia@mergington.edu"]
    },
    "Art Studio": {
        "description": "Painting, drawing, and visual arts exploration",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["noah@mergington.edu", "grace@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and critical thinking skills",
        "schedule": "Mondays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["ethan@mergington.edu"]
    },
    "Robotics Club": {
        "description": "Design, build, and program robots for competitions",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 14,
        "participants": ["maya@mergington.edu", "james@mergington.edu"]
    },
    "Tennis Team": {
        "description": "Learn tennis techniques and compete in matches",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["sarah@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Water sports, swimming lessons, and synchronized swimming",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["lucas@mergington.edu", "sophia@mergington.edu"]
    },
    "Music Band": {
        "description": "Learn instruments, ensemble performance, and concert preparation",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["david@mergington.edu", "anna@mergington.edu"]
    },
    "Photography Club": {
        "description": "Digital and film photography, photo editing, and gallery exhibitions",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 16,
        "participants": ["olivia@mergington.edu"]
    },
    "Science Club": {
        "description": "Explore physics, chemistry, and biology through hands-on experiments",
        "schedule": "Mondays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 18,
        "participants": ["noah@mergington.edu", "emma@mergington.edu"]
    },
    "Model United Nations": {
        "description": "Participate in international diplomacy simulations and debates",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["ethan@mergington.edu", "isabella@mergington.edu"]
    },
    "Volleyball Team": {
        "description": "Competitive volleyball league with drills and friendly matches",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 14,
        "participants": ["jessica@mergington.edu"]
    },
    "Track and Field": {
        "description": "Running, jumping, and throwing events with sprint and distance training",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["marcus@mergington.edu", "chloe@mergington.edu"]
    },
    "Dance Studio": {
        "description": "Contemporary, hip-hop, and ballet dance classes with performances",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["taylor@mergington.edu"]
    },
    "Sculpture Workshop": {
        "description": "3D art techniques including clay modeling, wood carving, and stone sculpting",
        "schedule": "Fridays, 2:00 PM - 4:00 PM",
        "max_participants": 12,
        "participants": ["jackson@mergington.edu", "lily@mergington.edu"]
    },
    "Philosophy Club": {
        "description": "Explore ethics, logic, and existential questions through Socratic discussions",
        "schedule": "Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 18,
        "participants": ["thomas@mergington.edu"]
    },
    "Math Olympiad": {
        "description": "Advanced problem-solving and mathematical competitions at regional and national levels",
        "schedule": "Wednesdays and Fridays, 4:00 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["victoria@mergington.edu", "ryan@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


    
