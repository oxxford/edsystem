from flask import send_file, request, Flask
from utils import get_speech
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/images/<string:name>', methods=['GET'])
def get_image(name):
    filename = './pictures/' + name
    return send_file(filename, mimetype='image/jpg')


@app.route('/audios/<string:name>', methods=['GET'])
def get_audio(name):
    filename = './audio/' + name
    return send_file(filename, mimetype='audio/mpeg')


if __name__ == '__main__':
    print(get_speech('We are going to win!'))
    app.run(host='0.0.0.0')
