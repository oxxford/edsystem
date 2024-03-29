from flask import send_file, request, Flask
from flask_cors import CORS
from utils import get_speech
# import CORS
from personalization import *
from flask import jsonify, send_from_directory
import json
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

from flask_cors import CORS
import os
async_mode = None


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
CORS(app)


@app.route('/js_files/<path:path>')
def send_js(path):
    return send_from_directory('js_files', path)


#   SOCKET FUNCTIONS

@socketio.on('canvas_to_server', namespace='/canvas')
def redirect_canvas(message):
    emit('canvas_to_teacher',
         message,
         broadcast=True)


@socketio.on('pagination_to_server', namespace='/pagination')
def redirect_canvas(message):
    emit('pagination_to_student',
         message,
         broadcast=True)

#      REST FUNCTIONS


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/get_tasks/<string:student_id>', methods=['GET'])
def get_tasks(student_id):
    tasks, res = get_student_tasks(student_id)
    for task in tasks:
        for page in task['pages']:
            if page['learner_type'] == 'audio':
                text = 'Question number ' + str(page['id']) + '. ' + page['question']
                page['question'] = '/audios/' + get_speech(text)

                for i, choice in enumerate(page['choices']):
                    text = 'Variant ' + str(i) + '. ' + choice['content']
                    choice['content'] = '/audios/' + get_speech(text)

    return jsonify(tasks)


@app.route('/get_student/<string:student_id>', methods=['GET'])
def get_student_info(student_id):
    student_filename = os.path.join(STUDENTS_FOLDER, student_id, f'{student_id}.json')
    with open(student_filename) as file:
        content = json.loads(file.read())
    return jsonify(content)


@app.route('/get_media', methods=['GET'])
def get_media():
    path = request.args.get('path')
    return send_file(path, mimetype='image/jpg')


@app.route('/give_hometasks/', methods=['POST'])
def post_tasks(task_path):
    '''
    task path: subjects/subject_name/lesson_name/tasks
    :param task_path:
    :return: code of success
    '''
    task_map, res = distribute_tasks(TASKS_FOLDER, STUDENTS_FOLDER)
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


@app.route('/get_audio', methods=['GET'])
def get_audio():
    path = request.args.get('path')
    return send_file(path, mimetype='audio/mpeg')


if __name__ == '__main__':
    # print(get_speech('To the door of an inn in the provincial town of N. there drew up a smart britchka—a light spring-carriage of the sort affected by bachelors, retired lieutenant-colonels, staff-captains, land-owners possessed of about a hundred souls, and, in short, all persons who rank as gentlemen of the intermediate category. In the britchka was seated such a gentleman—a man who, though not handsome, was not ill-favoured, not over-fat, and not over-thin. Also, though not over-elderly, he was not over-young. His arrival produced no stir in the town, and was accompanied by no particular incident, beyond that a couple of peasants who happened to be standing at the door of a dramshop exchanged a few comments with reference to the equipage rather than to the individual who was seated in it. “Look at that carriage,” one of them said to the other. “Think you it will be going as far as Moscow?” “I think it will,” replied his companion. “But not as far as Kazan, eh?” “No, not as far as Kazan.”'))
    # \\app.run(host='0.0.0.0')
    socketio.run(app, host='0.0.0.0', debug=True)
