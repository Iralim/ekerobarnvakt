from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_mail import Mail, Message
import requests
import os
import re
from markupsafe import escape
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config.from_pyfile('config.py')
mail = Mail(app)

RECAPTCHA_SECRET_KEY = os.getenv('RECAPTCHA_SECRET_KEY')
csrf = CSRFProtect(app)

limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

def is_valid_phone(phone):
    pattern = r"^\+?\d{7,15}$"
    return re.match(pattern, phone)

@app.route('/boka-barnvakt/', methods=['GET', 'POST'])
@limiter.limit("3 per minute")
def boka_barnvakt():
    if request.method == 'POST':
        name = escape(request.form.get('name', '').strip())
        phone = escape(request.form.get('phone', '').strip())
        email = escape(request.form.get('email', '').strip())
        description = escape(request.form.get('description', '').strip())
        recaptcha_response = request.form.get("g-recaptcha-response")

        if not name or not phone or not email:
            return jsonify({"message": "Alla fält måste fyllas i!"}), 400

        if not is_valid_email(email):
            return jsonify({"message": "Ogiltig e-postadress!"}), 400

        if not is_valid_phone(phone):
            return jsonify({"message": "Ogiltigt telefonnummer!"}), 400

        verify_url = "https://www.google.com/recaptcha/api/siteverify"
        payload = {"secret": RECAPTCHA_SECRET_KEY, "response": recaptcha_response}

        try:
            recaptcha_result = requests.post(verify_url, data=payload, timeout=5).json()
            if not recaptcha_result.get("success"):
                return jsonify({"message": "reCAPTCHA-verifiering misslyckades!"}), 400
        except requests.exceptions.RequestException:
            return jsonify({"message": "Ett fel uppstod vid verifieringen av reCAPTCHA!"}), 500

        subject = f"Ny bokning från {name}"
        body = f"""Namn: {name}\nTelefon: {phone}\nE-post: {email}\n\nBeskrivning:\n{description}"""
        msg = Message(subject, recipients=['info@iralim.com'], body=body)

        try:
            mail.send(msg)
            return jsonify({"message": "Din bokning har skickats!"})
        except Exception as e:
            return jsonify({"message": "Ett fel uppstod vid skickandet av din bokning. Försök igen!"}), 500

    return render_template('boka-barnvakt.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/favicon', 'favicon-32x32.png', mimetype='image/png')


@app.route('/')
def hem():
    return render_template('hem.html')

@app.route('/tjanster/')
def tjanster():
    return render_template('tjanster.html')

@app.route('/ansokan/')
def ansokan():
    return render_template('ansokan.html')
    
@app.route('/kvalite-och-sakerhet/')
def kvalite_och_sakerhet():
    return render_template('kvalite-och-sakerhet.html')

@app.route('/priser/')
def priser():
    return render_template('priser.html')

@app.route('/test/')
def test():
    return render_template('test.html')

@app.route('/om-oss/')
def om_oss():
    return render_template('om-oss.html')


if __name__ == '__main__':
    app.secret_key = "supersecretkey"  # Для flash-сообщений
    app.run(debug=True)