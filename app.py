from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# --- Static Data ---

schedule = {
    "monday": "No class on Monday.",
    "tuesday": "INFO2290 from 5–9.",
    "wednesday": "INFO2390 from 1–3 and INFO2400 from 5–9.",
    "thursday": "INFO2350 from 8–12.",
    "friday": "INFO2280 from 6–10.",
    "saturday": "No classes on Saturday.",
    "sunday": "No classes on Sunday."
}

contacts = {
    "INFO2290": "Darshvir Singh Dhingra – ddhingra@conestogac.on.ca",
    "INFO2400": "Abdul Samee – asamee@conestogac.on.ca",
    "INFO2280": "Tariq Mahmood – tmahmood@conestogac.on.ca",
    "INFO2350": "Nikola Cedic – Ncedic@conestogac.on.ca",
    "INFO2390": "Biljana Ivkovic – bivkovic@conestogac.on.ca"
}

deadlines = {
    "INFO2390": "Proof of Concept: June 18, Checkpoint 3: July 27, Build Book: July 30, Final Presentation: Aug 5.",
    "INFO2350": "Lab 3: July 3, Group Project: Aug 7.",
    "INFO2280": "Lab Book 2: June 17, Lab Book 3: Aug 6.",
    "INFO2400": "Project #1: June 15, Project #2: July 13, Project #3: Aug 9, Assignment #2: Aug 10.",
    "INFO2290": "Lab 1: June 22, Lab 2: July 8, Lab 3: July 22.",
    "general": "Next deadline: INFO2400 Mini Project #1, June 15. Fall registration: Aug 5. Applications: July 1."
}

test_schedules = {
    "INFO2390": "No upcoming tests.",
    "INFO2350": "Final Exam: Aug 14.",
    "INFO2280": "Test 2: June 20, Test 3: July 18, Final: Aug 15.",
    "INFO2400": "No upcoming tests.",
    "INFO2290": "Test 2: June 17, Test 3: July 15, Test 4: July 29, Final: Aug 11.",
    "next_test": "Next test: INFO2290 Test 2 on June 17."
}

# --- Utility Functions ---

def extract_weekday(query_text):
    for day in schedule.keys():
        if day in query_text.lower():
            return day
    return ""

def extract_course(query_text):
    pattern = re.compile(r'\binfo\d{4}\b', re.IGNORECASE)
    match = pattern.search(query_text)
    if match:
        return match.group(0).upper()
    return ""

# --- Webhook Endpoint ---

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    intent = req.get('queryResult', {}).get('intent', {}).get('displayName', '')
    parameters = req.get('queryResult', {}).get('parameters', {})
    query_text = req.get('queryResult', {}).get('queryText', '')

    # Get fallback values from raw text if entity is missing
    weekday = parameters.get('weekday', '').lower().strip() or extract_weekday(query_text)
    course = parameters.get('course_code', '').upper().strip() or extract_course(query_text)

    response_text = "I'm not sure how to help with that."

    if intent == "ask_schedule":
        response_text = schedule.get(weekday, f"I couldn't find your schedule for {weekday}.")

    elif intent == "ask_contact":
        response_text = contacts.get(course, f"Sorry, I don't have contact info for {course}.")

    elif intent == "ask_deadline":
        response_text = deadlines.get(course, deadlines["general"] if not course else f"No deadlines found for {course}.")

    elif intent == "ask_test_schedule":
        response_text = test_schedules.get(course, test_schedules["next_test"] if not course else f"No test schedule found for {course}.")

    return jsonify({ "fulfillmentText": response_text })

if __name__ == '__main__':
    app.run()

