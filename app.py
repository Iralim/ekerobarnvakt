from flask import Flask, request, render_template, jsonify, send_from_directory
from flask_mail import Mail, Message
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from database import add_rate_limit, is_ip_blocked

app = Flask(__name__)
app.config.from_pyfile('config.py')


mail = Mail(app)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

@app.before_request
def check_blocked_ip():
    if is_ip_blocked(get_remote_address()):
        return jsonify({"error": "Your IP has been blocked due to suspicious activity."}), 403

@app.route('/boka-barnvakt/', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def boka_barnvakt():
    ip = get_remote_address()

    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        description = request.form.get('description')

        if not name or not phone or not email:
            return jsonify({"message": "Alla fält måste fyllas i!"}), 400  

        subject = f"Ny bokning från {name}"
        body = f"""
        Namn: {name}
        Telefon: {phone}
        E-post: {email}

        Beskrivning:
        {description}
        """

        msg = Message(subject, recipients=['info@iralim.com'], body=body)

        try:
            mail.send(msg)
            add_rate_limit(ip, 5)  
            return jsonify({"message": "Din bokning har skickats!"})  
        except Exception as e:
            print(f"Error: {e}")
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
    app.run(debug=True)
