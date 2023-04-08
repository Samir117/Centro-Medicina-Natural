from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/principal')
def principal_page():
    return render_template('resumen.html')


@app.route('/sentimientos_emociones')
def sentimientos_emociones_page():
    return render_template('sentimientos_emociones.html')


@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

if __name__ == '__main__':
    app.run(debug=True)