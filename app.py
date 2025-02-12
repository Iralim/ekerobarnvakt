from flask import Flask, render_template, request, jsonify, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_pyfile('config.py')

mail = Mail(app)

@app.route('/boka-barnvakt/', methods=['GET', 'POST'])
def boka_barnvakt():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        description = request.form.get('description')

        if not name or not phone or not email:
            return jsonify({"message": "Alla fält måste fyllas i!"}), 400  # Возвращаем JSON-ошибку

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
            return jsonify({"message": "Din bokning har skickats!"})  # JSON-ответ для JS
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"message": "Ett fel uppstod vid skickandet av din bokning. Försök igen!"}), 500

    return render_template('boka-barnvakt.html')


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