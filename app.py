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
        [   r"mi nombre es (.*)", ["Hola %1, como estas ?",] ],

        [   r"Bien, y tu?", ["Excelente, listo para responder tus inquietudes",]],

        [   r"que es la medicina n(.*)?", ["Las medicina natural (o remedios herbales) son plantas usadas como medicamento."
             " Las personas las usan para ayudar a prevenir o curar una enfermedad.",]],

        [   r"que tan buena es la medicina n(.*)?", ["Genera efectos positivos a nivel emocional porque alivia el estrés, los miedos, la soledad,"
             " la desesperación, entre otros.",] ],

        [   r"por quien fuiste creado(.*)",  ["Mis creadores Son Estudiantes de Ing. en Sistemas. De la CUL",]],

        [   r"Para que fuiste creado(.*)",   ["Para ser tu asitente en todas las preguntas que tengas sobre Center Salud",]],

        [   r"En que lenguaje (.*) hecho(.*)?",   ["Fuí creado con librerias de lenguaje natural (NLTK),"
                                           " además mi base de programación es de Python",]],

        [   r"cual es tu nombre ?",     ["Mi nombre es Center ?",] ],

        [   r"como estas ?",   ["Bien, y tu?",]],

        [   r"disculpa (.*)",  ["No pasa nada",]],

        [   r"hola|hey|buenas|oye",   ["Hola", "Que tal",]],

        [   r"que (.*) quieres ?",  ["Que nos pongan 5 en el corte",]  ],

        [   r"(.*) creado ?",    ["Fui creado hoy",]],

        [   r"(.*)cancion(.*)",  ["Te podría gustar esta cancion "
                                  "https://www.youtube.com/watch?v=dhHh9cnmTOA&ab_channel=JoeArroyoVideo",] ],

        [   r"Alguna medicina para la tos|algun remedio para la tos(.*)?", ["Té con miel, Jengibre, abundante liquido",] ],

        [   r"Medicinas naturales(.*)", ["terapia neural, sueroterapia, homeopatía, campos magnéticos,"
                                         " biopuntura, ozonoterapia, acupuntura, quiropraxia, "
                                         "masaje terapéutico, entre otros.",]],

        [   r"remedios para cuidar(.*)", ["1. Aceitunas y limon para mareos."
                                          "2. Alcohol para quitar el olor de los pies,"
                                          " si quieres saber mas, pide tu cita "
                                          "a este numero telefonico 3004354010",]],

        [   r"que es center sal(.*)", ["Una plataforma dedicada a brindar soluciones de"
                                       " medicina natural para mejorar la calidad de vida de las personas.",]],

        [   r"para (.*) limon(.*)", ["ayuda a incrementar las defensas de nuestro cuerpo y "
                                     "a combatir diversas enfermedades",]],

        [   r"para (.*) ajo(.*)", ["ayuda combatir infecciones respiratorias, dilata los bronquios,"
                                   " fluidifica las mucosas, etc...",]],

        [   r"para (.*) sal(.*)", ["Es vital para el funcionamiento del organismo, consumirla en las cantidades"
                                   " recomendadas permite una adecuada función de los músculos y del corazón",]],

        [   r"(.*) acupuntura(.*)", ["Punción con una o más agujas que se realiza en una parte del cuerpo"
                                    " y tiene una finalidad curativa o terapéutica.",]],

        [   r"Cuales (.*) Hierbas medicinales", ["Agrego un link  de plantas medicinales y sus beneficios -->"
                                                " https://www.elmueble.com/plantas-flores/plantas-medicinales-que-puedes-cultivar-tu_42854",]],

        [   r"plantas de uso tradicional(.*)", ["Aqui encuentras las plantas mas utilizadas --->"
                                                "https://psicologiaymente.com/salud/plantas-medicinales",]],

        [   r"(.*) cita", ["Para agendar una cita, llame o escriba a este numero telefonico 3004354010",]],

        [   r"(.*)fin(.*)",   ["Chao" " Fue bueno hablar contigo",] ],

        [   r"(.*)", ["No entendí tu peticion o pregunta. Escribe nuevamente",]],

    ]

    chat = Chat(pares, mis_reflexions)
    entrada = request.form['entrada']
    respuesta = chat.respond(entrada)
    json = jsonify(respuesta)
    # envio a la base de datos
    cursor = db.connection.cursor()
    cursor.execute('INSERT INTO res_chatbot(entrada, respuesta) VALUES(%s, %s)', (entrada, respuesta))
    db.connection.commit()
    return json

if __name__ == '__main__':
    app.run(debug=True)