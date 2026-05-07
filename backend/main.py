from backend.utils.auth import register_user, login_user
from backend.services.genai import generate_ai_plan
from backend.services.feedback import apply_feedback
from backend.services.planner import generate_plan
from fastapi import FastAPI
from backend.models.user_model import User
from backend.utils.file_handler import save_user, load_user
from backend.services.memory_model import get_next_revision
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI Study Coach Backend Running"}


@app.post("/create-user")
def create_user(user: User):
    user_data = user.dict()

    # Add revision logic to each topic
    for subject in user_data["subjects"]:
        for topic in subject["topics"]:
            topic["next_revision"] = get_next_revision(topic["confidence"])

    save_user(user_data)

    return {
        "message": "User saved with revision schedule",
        "data": user_data
    }


@app.get("/get-user")
def get_user():
    return load_user()

@app.get("/get-plan")
def get_plan():
    user_data = load_user()

    if not user_data:
        return {"error": "No user data found"}

    plan = generate_plan(user_data)

    return {
        "message": "Daily study plan generated",
        "plan": plan
    }

@app.post("/submit-feedback")
def submit_feedback(subject: str, topic: str, score: int):
    user_data = load_user()

    if not user_data:
        return {"error": "No user found"}

    updated_data = apply_feedback(user_data, subject, topic, score)

    save_user(updated_data)

    return {
        "message": "Feedback applied successfully",
        "updated_data": updated_data
    }

@app.get("/get-ai-plan")
def get_ai_plan():
    user_data = load_user()

    if not user_data:
        return {"error": "No user data found"}

    plan = generate_plan(user_data)

    ai_response = generate_ai_plan(plan)

    return {
        "ai_plan": ai_response
    }

@app.post("/register")
def register(username: str, password: str):
    success = register_user(username, password)

    if success:
        return {"message": "User registered ✅"}
    else:
        return {"error": "User already exists"}


@app.post("/login")
def login(username: str, password: str):
    success = login_user(username, password)

    if success:
        return {"message": "Login successful ✅"}
    else:
        return {"error": "Invalid credentials"}