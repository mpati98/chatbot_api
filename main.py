from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from chat import get_response

app = Flask(__name__)
api = Api(app)

output = {}

# def Model_init():
#     # import model from the model file can be pretrained or fine tuned

#     blender_agent = create_agent_from_model_file(
#         "zoo:blender/blender_90M/model")
#     return blender_agent

# Argument parsing
parser = reqparse.RequestParser()
parser.add_argument('q', help="Type your question")
class Chatbot(Resource):

    def get(self):
        # Use parser and find the user's query
        args = parser.parse_args()
        sentence = args['q']
        try:
            print(sentence)
            resp, tag = get_response(sentence)
            print(resp, tag)
            if tag == 'unknown_response':
                # blender_agent.observe({'text': text_to_sys, 'episode_done': False})
                # response = blender_agent.act()  # From bot
                # print(response)
                res = [
                    "None",
                    "default/golfActivitiesInfor04"
                ]
                # tts_fptAI(res)
                # SpeakText(res)
                res_text = res[0]
                res_audio = res[1]
            else:
                # res = event_response(tag=tag)
                # if res == "None":
                res = resp
                print(res)
                res_text = res[0]
                res_audio = res[1]
        except:
            res = [
                    "Bạn có thể liên hệ Miss Phương Trinh là Thư ký CLB qua số 0388 372 691 để biết thêm về thông tin này",
                    "default/golfActivitiesInfor04"
                ]
                # tts_fptAI(res)
                # SpeakText(res)
            res_text = res[0]
            res_audio = res[1]
        output = {
            "res_text": res_text,
            "res_audio": res_audio
        }
        return jsonify(output)
    
api.add_resource(Chatbot, '/response')

if __name__ == "__main__":
    app.run(debug=True)