from datetime import datetime, timedelta


# 🔹 Decide revision gaps based on confidence
def get_revision_gaps(confidence):
    if confidence <= 2:
        return [1, 2, 4, 7]
    elif confidence == 3:
        return [1, 3, 5, 10]
    else:
        return [2, 5, 10, 15]


# 🔹 Generate revision schedule
def generate_revision_schedule(confidence):
    today = datetime.now()
    gaps = get_revision_gaps(confidence)

    schedule = []
    for gap in gaps:
        next_date = today + timedelta(days=gap)
        schedule.append(next_date.strftime("%Y-%m-%d"))

    return schedule


# 🔹 Get next revision date (first one)
def get_next_revision(confidence):
    return generate_revision_schedule(confidence)[0]