from datetime import datetime

def calculate_priority(topic, exam_date):
    today = datetime.now().strftime("%Y-%m-%d")

    exam = datetime.strptime(exam_date, "%Y-%m-%d")
    days_left = (exam - datetime.now()).days

    # 🔥 CORE FACTORS
    weakness = 5 - topic["confidence"]   # BIG impact
    difficulty = topic["difficulty"]
    urgency = max(0, 15 - days_left)

    # 🔥 STRONGER REVISION LOGIC
    # 
    revision_bonus = 0
    if topic.get("next_revision"):
        if topic["next_revision"] <= today:
            revision_bonus = 8   # 🔥 make it strong

    # 🎯 FINAL SCORE
    priority = (weakness * 3) + (difficulty * 2) + urgency + revision_bonus

    return priority

# 🔹 Generate full plan
def generate_plan(user_data):
    plan = []

    for subject in user_data["subjects"]:
        for topic in subject["topics"]:

            score = calculate_priority(topic, user_data["exam_date"])

            plan.append({
                "subject": subject["name"],
                "topic": topic["name"],
                "priority": score,
                "confidence": topic["confidence"]
            })

    # 🔥 Sort highest priority first
    sorted_plan = sorted(plan, key=lambda x: x["priority"], reverse=True)

    return sorted_plan