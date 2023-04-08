from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
x= "soy muy feliz"
t = TextBlob(x) 
sid = SentimentIntensityAnalyzer()
resultados = sid.polarity_scores(str (t.translate(from_lang= "es",to="en")))

print(resultados)


