from flask import Flask, render_template, jsonify, request
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()  # Load environment variables

app = Flask(__name__)

# Database connection
try: 
    db = mysql.connector.connect(
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_NAME")
    )
    print("Database connection successful")

except mysql.connector .Error as err:
    print(f"Error: {err}")
    exit(1)

# Route to load html file
@app.route('/')
def home():
    return render_template("index.html")

#
@app.route('/api/irrigate', methods=['POST'])
def control_irrigation():
    data = request.json
    action = data.get('action')  # 'start' or 'stop'
    crop = data.get('crop')

# Validate input
    if not action or not crop:
        return jsonify({"status": "Error", "message": "Missing 'action' or 'crop' in the request"}), 400
    
    # Logic to determine irrigation status based on thresholds
    cursor = db.cursor()
    cursor.execute("SELECT * FROM crop_water_requirements WHERE crop=%s", (crop,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return jsonify({"status": "Error", "message": "Crop not found"}), 404
    
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

