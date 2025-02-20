from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_mail import Mail, Message
import requests
import os
from markupsafe import escape
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config.from_pyfile('config.py')
mail = Mail(app)

RECAPTCHA_SECRET_KEY = os.getenv('RECAPTCHA_SECRET_KEY')
csrf = CSRFProtect(app)



@app.route('/boka-barnvakt/', methods=['GET', 'POST'])
def boka_barnvakt():
    if request.method == 'POST':
    
        name = escape(request.form.get('name', '').strip())
        phone = escape(request.form.get('phone', '').strip())
        email = escape(request.form.get('email', '').strip())
        description = escape(request.form.get('description', '').strip())
        recaptcha_response = request.form.get("g-recaptcha-response")

        if not name or not phone or not email:
            return jsonify({"message": "Alla fält måste fyllas i!"}), 400

        # Проверка reCAPTCHA
        verify_url = "https://www.google.com/recaptcha/api/siteverify"
        payload = {"secret": RECAPTCHA_SECRET_KEY, "response": recaptcha_response}

        try:
            recaptcha_result = requests.post(verify_url, data=payload, timeout=5).json()
            if not recaptcha_result.get("success"):
                return jsonify({"message": "reCAPTCHA-verifiering misslyckades!"}), 400
        except requests.exceptions.RequestException as e:
            print(f"reCAPTCHA-fel: {e}")
            return jsonify({"message": "Ett fel uppstod vid verifieringen av reCAPTCHA!"}), 500

    
        subject = f"Ny bokning från {name}"
        body = f"""Namn: {name}
Telefon: {phone}
E-post: {email}

Beskrivning:
{description}
"""
        msg = Message(subject, recipients=['info@iralim.com'], body=body)

        try:
            mail.send(msg)
            return jsonify({"message": "Din bokning har skickats!"})
        except Exception as e:
            print(f"E-postfel: {e}")
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