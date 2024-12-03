from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()  # Load environment variables

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host = os.getenv("DB_HOST"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    database = os.getenv("DB_NAME")
)

@app.route('/irrigate', methods=['POST'])
def control_irrigation():
    data = request.json
    action = data.get('action')  # 'start' or 'stop'
    crop = data.get('crop')
    
    # Logic to determine irrigation status based on thresholds
    cursor = db.cursor()
    cursor.execute("SELECT * FROM crop_water_requirements WHERE crop=%s", (crop,))
    result = cursor.fetchone()

    if action == 'start':
        # Send command to microcontroller
        return jsonify({"status": "Irrigation started"})
    elif action == 'stop':
        # Send command to microcontroller
        return jsonify({"status": "Irrigation stopped"})
    else:
        return jsonify({"status": "Invalid action"})

if __name__ == '__main__':
    app.run(debug=True)

