from flask import send_file, request, Flask
from utils import get_speech
from personalization import *
from flask import jsonify
import json
import os
app = Flask(__name__)
import socket
print(socket.gethostbyname(socket.gethostname()))
# export FLASK_RUN_PORT=3000

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/get_tasks/<string:student_id>', methods=['GET'])
def get_tasks(student_id):
    tasks, res = get_student_tasks(student_id)
    for task in tasks:
        for page in task['pages']:
            if page['learner_type'] == 'audio':
                text = 'Question number ' + str(page['id']) + '. ' + page['question'] + ''
                page['question'] = '/audios/' + get_speech(text)

                for choice in page['choices']:
                    text = 'Variant 1. ' + choice['content']
                    choice['content'] = '/audios/' + get_speech(text)

    print(res)
    return jsonify(tasks)



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
    task_map ,res = distribute_tasks(TASKS_FOLDER, STUDENTS_FOLDER)
    if res < 1:
        return 500
    save_tasks(task_map, STUDENTS_FOLDER)
    return 200

@app.route('/lesson_content/<string:name>', methods=['GET'])
def get_lesson_content(name):
    lesson_filename = os.path.join(SUBJECT_FOLDER, name, f'{name}.json')
    with open(lesson_filename) as file:
        lesson_content = json.loads(file.read())
    return jsonify(lesson_content)




@app.route('/audios/<string:name>', methods=['GET'])
def get_audio(name):
    filename = './audio/' + name
    return send_file(filename, mimetype='audio/mpeg')


if __name__ == '__main__':
    # print(get_speech('We are going to win!'))
    app.run(host='0.0.0.0')
