from flask import Flask, jsonify, request, render_template, send_file, send_from_directory, abort
from flask_cors import CORS
import pickle
import os
import smtplib
import ssl
from email.message import EmailMessage

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

users_db_file = "users.pkl"
booked_slots_file = "booked_slots.pkl"

# Global variable to store nearest spot
nearest_spot = None

def load_users():
    try:
        with open(users_db_file, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}

def load_slots():
    try:
        with open(booked_slots_file, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}

users = load_users()
booked_slots = load_slots()

# Function to send an email
# def send_email(signup_details):
#     email_sender = 'parksense.info@gmail.com'
#     email_password = 'eiuzybzwqzgllnij'
#     email_receiver = 'agileninja01@gmail.com'

#     subject = 'New Signup Notification'
#     body = f"""
#     New user signed up with the following details:
#     Name: {signup_details['fullname']}
#     Email: {signup_details['email']}
#     Phone: {signup_details['phone']}
#     Age: {signup_details['age']}
#     Gender: {signup_details['gender']}
#     """

#     em = EmailMessage()
#     em['From'] = email_sender
#     em['To'] = email_receiver
#     em['Subject'] = subject
#     em.set_content(body)

#     context = ssl.create_default_context()

#     with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
#         smtp.login(email_sender, email_password)
#         smtp.sendmail(email_sender, email_receiver, em.as_string())

# @app.route('/')
# def home():
#     return render_template('index.html')

@app.route('/get_latest_parking_image', methods=['GET'])
def get_latest_parking_image():
    image_path = os.path.join(os.getcwd(), 'parking_status.jpg')
    if os.path.exists(image_path):
        try:
            return send_file(image_path, mimetype='image/jpg')
        except FileNotFoundError:
            return jsonify({"status": "Image not found"}), 404
    else:
        return jsonify({"status": "Image not found"}), 404

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    
    if username in users and users[username] == password:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "failure"}), 401

@app.route('/book_slot', methods=['POST'])
def book_slot():
    data = request.json
    slot = data['slot']
    username = data['username']
    
    if not slot.startswith("slot") or not 1 <= int(slot[4:]) <= 69:
        return jsonify({"status": "invalid slot"}), 400

    if slot not in booked_slots:
        booked_slots[slot] = username
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "already booked"}), 400

@app.route('/get_nearest_spot', methods=['GET'])
def get_nearest_spot():
    global nearest_spot
    if nearest_spot:
        return jsonify({"nearest_spot": nearest_spot}), 200
    else:
        return jsonify({"nearest_spot": "No empty spots"}), 200

# @app.route('/signup')
# def signup_form():
#     return render_template('signup.html')


# @app.route('/signup', methods=['POST'])
# def signup():
#     data = request.json
#     # Here you can add code to save the user data if needed
#     # For demonstration, directly sending the email
#     send_email(data)
#     return jsonify({"message": "Signup successful, email sent."}), 200

@app.route('/booking_confirmation')
def booking_confirmation():
    return render_template('booking_confirmation.html')

if __name__ == '__main__':
    app.run(debug=True)

