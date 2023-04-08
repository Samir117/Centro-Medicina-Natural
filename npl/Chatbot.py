from nltk.chat.util import Chat

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
def chatear():
    print("Hola samir acaba ropa") #mensaje por defecto
    chat = Chat(pares, mis_reflexions)
    user_input = "hola"
    print('hi', chat.respond(user_input))
    user_input = "como estas"
    print('hi', chat.respond(user_input))
    user_input = "cuando fuiste creado"
    print('hi', chat.respond(user_input))
if __name__ == "__main__":
    chatear()

