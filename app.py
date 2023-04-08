# librerias a utilizar
from flask import Flask, render_template, request, jsonify
import re
import urllib.request
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import urllib.request
from inscriptis import get_text
from nltk import word_tokenize,sent_tokenize
import heapq
from textblob import TextBlob
from flask_mysqldb import MySQL
from nltk.chat.util import Chat
# elementos adicionales y necesarios de ntl para resumen
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'center_salud'
db = MySQL(app)

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

@app.route('/api_resumen', methods=['POST'])
def api_resumen():
    if request.method == 'POST':
        try:
            if request.form['link'] and request.form['traduccion']:
                # recoleccion de informacion
                link = request.form['link']
                traduccion = bool(request.form['traduccion'])
                minLetters = 70
                # procesamiento del link para scraping
                html =urllib.request.urlopen(link).read().decode('utf-8')
                text = get_text(html)
                article_text =  text
                article_text = article_text.replace("[edit]","")

                ##Elimina caracteres especiales y espacios
                article_text = re.sub(r'\[[0-9]*\]',' ', article_text)
                article_text = re.sub(r'\s+',' ',article_text)

                formatted_article_text = re.sub('[^a-zA-Z]',' ',article_text)
                formatted_article_text= re.sub(r'\s+',' ',formatted_article_text)

                ##tokenizacion
                sentence_list =nltk.sent_tokenize(article_text)     

                ##Separa palabra y frecuencia
                stopwords = nltk.corpus.stopwords.words('english')

                word_frequencies = {}
                for word in nltk.word_tokenize(formatted_article_text):
                    if word not in stopwords:
                        if word not in word_frequencies.keys():
                            word_frequencies[word] = 1
                        else:
                            word_frequencies[word]+=1
            
                maximun_frequency = max(word_frequencies.values())
                for word in word_frequencies.keys():
                    word_frequencies[word] = (word_frequencies[word]/maximun_frequency)
        
        
                ## frases que se repiten
                sentence_scores = {}
                for sent in sentence_list:
                    for word in nltk.word_tokenize(sent.lower()):
                        if word in word_frequencies.keys():
                            if len(sent.split(' ')) < minLetters:
                                if sent not in sentence_scores.keys():
                                    sentence_scores[sent] = word_frequencies[word]
                                else :
                                    sentence_scores[sent] += word_frequencies[word]
                
                summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
                # variables para encapsular los textos de resumen y traducidos
                summary = ' '.join(summary_sentences)
                summary_tr = ''

                if not traduccion:
                    return jsonify(str(summary))
                else:
                    traduc=TextBlob(summary)
                    summary_tr = traduc.translate(from_lang="en" , to ="es")
                    # luego de traducir devolvemos un arreglo para jsonify
                    data = {
                        'original': str(summary),
                        'traducido': str(summary_tr)
                    }
                # por ultimo hacemos la insercion
                cursor = db.connection.cursor()
                cursor.execute('INSERT INTO resumenes(link, original, traducido) VALUES(%s, %s, %s)', (link, summary, str(summary_tr).encode('utf-8')))
                db.connection.commit()
                # RETORNAMOS
                return jsonify(data)
                
            else:
                return []
            
        except Exception as e:
            print(e)
            return []

@app.route('/api_sentimientos', methods=['POST'])
def api_sentimientos():
    # validamos el metodo
    if request.method == 'POST':
        try:
            expresion = request.form['expresion']
            # luego de obtener el dato lo ingresamos a la libreria 
            t = TextBlob(expresion)
            sid = SentimentIntensityAnalyzer()
            resultados = sid.polarity_scores(str(t.translate(from_lang= "es",to="en")))
            cursor = db.connection.cursor()
            cursor.execute('INSERT INTO analisis_sentimiento(positivo, negativo, neutro, compuesto) VALUES(%s, %s, %s, %s)', (resultados['pos'], resultados['neg'], resultados['neu'], resultados['compound']))
            db.connection.commit()
            return jsonify(resultados)
        
        except Exception as e:
            print(e)
            return []

@app.route('/api_chatbot', methods=['POST'])
def api_chatbot():
    mis_reflexions = {
        "ir": "fui",
        "hola": "hey"
    }

    pares = [
        [
            r"mi nombre es (.*)",
            ["Hola %1, como estas ?",]
        ],
        [
            r"cual es tu nombre ?",
            ["Mi nombre es Chatbot ?",]
        ],
        [
            r"como estas ?",
            ["Bien, y tu?",]
        ],
        [
            r"disculpa (.*)",
            ["No pasa nada",]
        ],
        [
            r"hola|hey|buenas",
            ["Hola", "Que tal",]
        ],
        [
            r"que (.*) quieres ?",
            ["Nada gracias",]
            
        ],
        [
            r"(.*) creado ?",
            ["Fui creado hoy",]
        ],
        [
            r"finalizar",
            ["Chao","Fue bueno hablar contigo"]
        ],
    ]

    chat = Chat(pares, mis_reflexions)
    entrada = request.form['entrada']
    respuesta = chat.respond(entrada)
    # envio a la base de datos
    cursor = db.connection.cursor()
    cursor.execute('INSERT INTO res_chatbot(entrada, respuesta) VALUES(%s, %s)', (entrada, respuesta))
    db.connection.commit()
    return respuesta

if __name__ == '__main__':
    app.run(debug=True)