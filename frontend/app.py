import requests
import streamlit as st
import plotly.express as px # type: ignore
import pandas as pd

# ADD THIS RIGHT AFTER IMPORTS
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
st.title("🔐 Login System")

menu = ["Login", "Signup"]
choice = st.sidebar.selectbox("Menu", menu)

if not st.session_state.logged_in:

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Signup":
        if st.button("Create Account"):
            res = requests.post(
                "http://127.0.0.1:8001/register",
                params={"username": username, "password": password}
            )
            st.write(res.text)

    elif choice == "Login":
        if st.button("Login"):
            res = requests.post(
                "http://127.0.0.1:8001/login",
                params={"username": username, "password": password}
            )

            if "message" in res.json():
                st.session_state.logged_in = True
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials")

    st.stop()

st.markdown("""
<style>
body {
    background-color: #0e1117;
}
</style>
""", unsafe_allow_html=True)
st.set_page_config(page_title="AI Study Coach", layout="wide")

# HEADER
st.markdown("""
# 🧠 AI Cognitive Study Coach
### 🚀 Smart Learning | Adaptive Planning | AI Guidance
""")

st.divider()
# SIDEBAR
st.sidebar.title("⚙️ Settings")
st.sidebar.write("Customize your study inputs")

name = st.sidebar.text_input("Name")
exam_date = st.sidebar.date_input("Exam Date")
daily_hours = st.sidebar.slider("Daily Study Hours", 1, 10)

# INPUT SECTION
st.subheader("📋 Enter Subject Details")

col1, col2 = st.columns(2)

with col1:
    subject = st.text_input("Subject")

with col2:
    topic = st.text_input("Topic")

col3, col4 = st.columns(2)

with col3:
    difficulty = st.slider("Difficulty", 1, 5)

with col4:
    confidence = st.slider("Confidence", 1, 5)
# SAVE BUTTON

if st.button("💾 Save Data", use_container_width=True):
    data = {
        "name": name,
        "exam_date": str(exam_date),
        "daily_hours": daily_hours,
        "subjects": [
            {
                "name": subject,
                "topics": [
                    {
                        "name": topic,
                        "difficulty": difficulty,
                        "confidence": confidence
                    }
                ]
            }
        ]
    }

    res = requests.post(
    "http://127.0.0.1:8001/create-user",
    json=data
)
    if res.status_code == 200:
        st.success("✅ Data saved successfully!")
    else:
        st.error("❌ Error saving data")

st.divider()
# PLAN SECTION
import pandas as pd

st.subheader("📅 Study Plan")

if st.button("Generate Plan 📊"):
    res = requests.get("http://127.0.0.1:8001/get-plan")

    if res.status_code == 200:
        plan = res.json()["plan"]

        # SHOW PLAN
        for item in plan:
            with st.container():
                st.markdown(f"""
                ### 📘 {item['topic']} ({item['subject']})
                - 🔥 Priority: **{item['priority']}**
                - 🎯 Confidence: **{item['confidence']}**
                """)
                st.divider()

        # ADD CHART HERE (INSIDE BLOCK)
        df = pd.DataFrame(plan)

        st.subheader("📊 Priority Distribution")

        fig = px.pie(
        df,
        names="topic",
        values="priority",
        title="Study Priority Distribution",
        hole=0.4   # 🔥 makes donut chart
        )

        # Progress bars (intuitive)
        for item in plan:
            st.write(f"📘 {item['topic']}")
            st.progress(min(item["priority"] / 20, 1.0))

        # Chart (visual comparison)
        st.plotly_chart(fig)

    else:
        st.error("Error generating plan")

# AI SECTION
st.subheader("🤖 AI Coach Insights")

if st.button("Get AI Guidance"):
    res = requests.get("http://127.0.0.1:8001/get-ai-plan")

    if res.status_code == 200:
        st.markdown("### 💡 Personalized Suggestions")
        st.info(res.json()["ai_plan"])

# FEEDBACK
st.subheader("🔁 Feedback System")

col5, col6 = st.columns(2)

with col5:
    fb_subject = st.text_input("Subject (feedback)")

with col6:
    fb_topic = st.text_input("Topic (feedback)")

fb_score = st.slider("Understanding %", 0, 100)

if st.button("Submit Feedback"):
    params = {
        "subject": fb_subject,
        "topic": fb_topic,
        "score": fb_score
    }

    res = requests.post("http://127.0.0.1:8001/submit-feedback", params=params)

    if res.status_code == 200:
        st.success("✅ Feedback submitted!")
    else:
        st.error("Error submitting feedback")

if st.session_state.logged_in:
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()


