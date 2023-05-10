from flask import Flask, jsonify, render_template, request
from flask_restful import Resource, Api
import nltk
nltk.download('popular')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

# Load data
from keras.models import load_model
model = load_model('model.h5')
import json
import random
intents = json.loads(open('data/data.json').read())
words = pickle.load(open('texts.pkl','rb'))
classes = pickle.load(open('labels.pkl','rb'))

def transText(text_input, scr_input='user'):
    from googletrans import Translator
    # define a translate object
    translate = Translator()
    if scr_input == "bot":
        result = translate.translate(text_input, src='en', dest='vi')
        result = result.text
    elif scr_input == "user":
        result = translate.translate(text_input, src='vi', dest='en')
        result = result.text
    else:
        result = "We not support this language, please use English or Vietnamese!"
    return result

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


app = Flask(__name__)
api = Api(app)



@app.route("/")
def home():
    return render_template("index.html")

@app.route('/welcome', methods=["POST"])
def voice_welcome():
    welcome = "Xin chào, tôi là trợ lý ảo Ban công tác xã hội của câu lạc bộ Doanh nhân Sài Gòn, tôi có thẻ giúp gì cho bạn?"
    res = {
        "msg": welcome,
        "audio": "data/audio/default/introduce.mp3"
    }
    return jsonify(res)


class Chatbot(Resource):

    def post(self):

        text_input = request.get_json().get("message")
        text_input = transText(text_input)
        resp = chatbot_response(text_input)
        output = {
            "res_text": resp,
            # "res_audio": res_audio
        }
        return jsonify(output)

api.add_resource(Chatbot, '/response')

if __name__ == "__main__":
    app.run(debug=True)