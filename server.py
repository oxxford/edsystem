from flask import send_file, request, Flask
from utils import get_speech, get_my_ip
from personalization import *
from flask import jsonify
import json
import os
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/images/<string:name>', methods=['GET'])
def get_image(name):
    filename = './pictures/' + name
    return send_file(filename, mimetype='image/jpg')

@app.route('/give_hometasks/', methods=['POST'])
def post_tasks(task_path):
    '''
    task path: subjects/subject_name/lesson_name/tasks
    :param task_path:
    :return: code of success
    '''
    a = 0

@app.route('/lesson_content/<string:name>', methods=['GET'])
def get_lesson_content(name):
    lesson_filename = os.path.join(SUBJECT_FOLDER, name, f'{name}.json')
    ip = get_my_ip()
    with open(lesson_filename) as file:
        lesson_content = json.loads(file.read())
        """
        for page in lesson_content['pages']:
            print(page)
            for content in page['content']:
                if content['type'] == 'image' or content['type'] == 'audio' or content['type'] == 'video':
                    content['content'] = 'http://' + ip + ':5000' + content['content']
        """
    return jsonify(lesson_content)




@app.route('/audios/<string:name>', methods=['GET'])
def get_audio(name):
    filename = './audio/' + name
    return send_file(filename, mimetype='audio/mpeg')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
