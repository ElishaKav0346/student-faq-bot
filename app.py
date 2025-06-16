from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    
    weekday = req.get('queryResult', {}).get('parameters', {}).get('weekday', '').lower()
    
    schedule = {
        "tuesday": "INFO2290 from 5–9",
        "wednesday": "INFO2390 from 1–3, INFO2400 from 5–9",
        "thursday": "INFO2350 from 8–12",
        "friday": "INFO2280 from 6–10"
    }

    response_text = schedule.get(weekday, f"Sorry, I couldn't find a class scheduled for {weekday.title()}.")

    return jsonify({
        "fulfillmentText": response_text
    })

if __name__ == '__main__':
    app.run(debug=True)
