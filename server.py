from flask import send_file, request, Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/images/<string:name>.jpg', methods=['GET'])
def get_image(name):
    filename = './pictures/' + name + '.jpg'
    return send_file(filename, mimetype='image/jpg')

@app.route('/give_hometasks', methods=['POST'])
def post_tasks(task_path):
    '''
    task path: subjects/subject_name/lesson_name/tasks
    :param task_path:
    :return: code of success
    '''



if __name__ == '__main__':
    app.run(host='0.0.0.0')
