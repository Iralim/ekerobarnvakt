from flask import Flask, render_template

app = Flask(__name__)

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

@app.route('/boka-barnvakt/')
def boka_barnvakt():
    return render_template('boka-barnvakt.html')

@app.route('/test/')
def test():
    return render_template('test.html')

@app.route('/om-oss/')
def om_oss():
    return render_template('om-oss.html')


if __name__ == '__main__':
    app.run(debug=True)