from flask import Flask, jsonify, render_template, request
from flask_restful import Resource, Api
from utils import tts_fptAI, play_mp3


app = Flask(__name__)
api = Api(app)


# def Model_init():
#     # import model from the model file can be pretrained or fine tuned

#     blender_agent = create_agent_from_model_file(
#         "zoo:blender/blender_90M/model")
#     return blender_agent
# Load speech data from fpt server
url = 'https://api.fpt.ai/hmi/tts/v5'
payload = ''
headers = {
    'api-key': 'OaGgkRmCMzOoZbnwgX70IDWo77t0g5SW',
    'speed': '',
    'voice': 'banmai'
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/welcome', methods=["GET"])
def voice_welcome():
    welcome = "Xin chào, tôi là trợ lý ảo Ban công tác xã hội của câu lạc bộ Doanh nhân Sài Gòn, tôi có thẻ giúp gì cho bạn?"
    audio = tts_fptAI(welcome)
    play_mp3("data/audio/" + audio)
    return jsonify(welcome)


class Chatbot(Resource):

    def get(self):
        # Use parser and find the user's query
        # args = parser.parse_args()
        # sentence = args['q']
        text_input = request.get_json().get("message")
        # try:
        #     print(text_input)
        #     re
        # except:
        #     res = [
        #             "Bạn có thể liên hệ Miss Phương Trinh là Thư ký CLB qua số 0388 372 691 để biết thêm về thông tin này",
        #             # "default/golfActivitiesInfor04"
        #         ]
        #         # tts_fptAI(res)
        #         # SpeakText(res)
        #     res_text = res[0]
        #     # res_audio = res[1]
        output = {
            "res_text": text_input,
            # "res_audio": res_audio
        }
        return jsonify(output)

api.add_resource(Chatbot, '/response')

if __name__ == "__main__":
    app.run(debug=True)