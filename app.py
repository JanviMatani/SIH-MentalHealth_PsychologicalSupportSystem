from flask import Flask
from dotenv import load_dotenv
import os
import mysql.connector
from flask import Flask, render_template, request, jsonify


load_dotenv()
app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = db.cursor()

@app.route("/")
def home():
    return render_template("Booking.html")

@app.route("/book", methods=["POST"])
def book():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON received"}), 400

    lang = data.get("language")
    mode = data.get("mode")
    date = data.get("date")
    time_slot = data.get("time")

    if not all([lang, mode, date, time_slot]):
        return jsonify({"status": "error", "message": "All fields are required"}), 400

    sql = "INSERT INTO appointments (language, mode, date, time_slot) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (lang, mode, date, time_slot))
    db.commit()

    return jsonify({"status": "success", "message": "Appointment booked!"})
@app.route("/booked_times")
def booked_times():
    date = request.args.get("date")
    if not date:
        return jsonify([])

    cursor.execute("SELECT time_slot FROM appointments WHERE date = %s", (date,))
    booked = [row[0] for row in cursor.fetchall()]
    return jsonify(booked)


if __name__ == "__main__":
    app.run(debug=True)
