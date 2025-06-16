from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    # Extract the weekday entity
    weekday_raw = req.get('queryResult', {}).get('parameters', {}).get('weekday', '')
    weekday = weekday_raw.strip().lower().replace("on ", "").rstrip("s")  # Normalize input

    print("Received weekday (raw):", weekday_raw)
    print("Sanitized weekday:", weekday)

    # Class schedule dictionary
    schedule = {
        "monday": "No class on Monday.",
        "tuesday": "INFO2290 from 5–9.",
        "wednesday": "INFO2390 from 1–3 and INFO2400 from 5–9.",
        "thursday": "INFO2350 from 8–12.",
        "friday": "INFO2280 from 6–10.",
        "saturday": "No classes on Saturday.",
        "sunday": "No classes on Sunday."
    }

    # Get the response or fallback
    response = schedule.get(weekday, "I couldn't find your schedule for that day.")

    return jsonify({
        "fulfillmentText": response
    })

if __name__ == '__main__':
    app.run()


