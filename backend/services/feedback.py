from backend.services.memory_model import get_next_revision


# 🔹 Update confidence based on feedback
def update_confidence(topic, feedback_score):
    if feedback_score >= 80:
        topic["confidence"] += 1
    elif feedback_score <= 50:
        topic["confidence"] -= 1

    # Keep within limits
    topic["confidence"] = max(1, min(5, topic["confidence"]))

    return topic


from backend.services.memory_model import get_next_revision

def apply_feedback(user_data, subject_name, topic_name, feedback_score):
    for subject in user_data["subjects"]:
        if subject["name"].lower() == subject_name.lower():

            for topic in subject["topics"]:
                if topic["name"].lower() == topic_name.lower():

                    # 🔥 UPDATE CONFIDENCE
                    if feedback_score >= 80:
                        topic["confidence"] += 1
                    elif feedback_score <= 50:
                        topic["confidence"] -= 1

                    topic["confidence"] = max(1, min(5, topic["confidence"]))

                    # 🔥 UPDATE REVISION
                    topic["next_revision"] = get_next_revision(topic["confidence"])

                    print("UPDATED TOPIC:", topic)  # DEBUG

    return user_data