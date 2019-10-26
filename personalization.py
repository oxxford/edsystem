
import uuid
import glob
import os
import json
from typing import Dict, List
from termcolor import colored
from os import path
STUDENTS_FOLDER = 'students/grade 1/A'
SUBJECT_FOLDER = 'subjects/literature_4_2019'
LEARNER_CODE = {'audio': 2, 'visual':1}
TASKS_FOLDER = 'subjects/literature_4_2019/lesson1/tasks'
def get_all_students(students_path):
    if not os.path.exists(students_path):
        print(colored(f'No such folder {students_path}', 'red'))
        return [], -1
    students = [] # list of dicts
    students_files = []
    students_folders = glob.glob(f'{students_path}/*')
    students_folders = [folder for folder in students_folders if '.' not in folder]
    for folder in students_folders:
        files = glob.glob(folder + '/*.json')
        students_files.extend(files)
    # students_files = glob.glob(os.path.join(students_path, '/'))
    if len(students_files) ==0:
        print(colored('no students', 'red'))
        return [], 0
    for student_file in students_files:
        with open(student_file) as file:
            content = json.loads(file.read())
            students.append(content)
    return students, 1


def set_task(task:List, students_ids: [], tasks_map:{}):
    tasks_map = tasks_map.copy()
    for student_id in tasks_map.keys():
        if student_id in students_ids:
            tasks_map[student_id].append({'pages': task})
    return tasks_map

def distribute_tasks(tasks_path, students_path):
    '''

    :param tasks_path:
    :return: Dist of tasks map: student:[tasks], status 1 - ok, 0 - not ok
    -1 - wrong path
    0 - empty list of tasks
    '''
    if not os.path.exists(tasks_path):
        return {}, -1
    tasks_files = glob.glob(tasks_path + '/*.json')
    if len(tasks_files) == 0:
        return  {}, 0
    students, res = get_all_students(students_path)
    if res < 1:
        return {}, res
    students_map = {}
    leaner_type_map = {} # type ->[student_ids]
    # learner_type_tasks = {}

    for student in students:
        student_id = student['student_id']
        type = student['learner_type']
        students_map[student_id] = student
        if not type in leaner_type_map:
            leaner_type_map[type] = [student_id]
        else:
            leaner_type_map[type].append(student_id)
    task_map = {student_id: [] for student_id in students_map.keys()} # [] list of tasks. where task is a array of obj from pages {}
    for task_file in tasks_files:
        with open(task_file) as file:
            tasks = json.loads(file.read())
        tasks_type = tasks['type']
        if tasks_type == 'test_set':
            curr_task = tasks['pages'] # then we send this task to all students
            task_map = set_task(curr_task, students_ids=students_map.keys(), tasks_map=task_map) # assigns task to each student
        else:  # this file contains variants for different variants of tasks
            task_variants = tasks['pages']
            for task_v in task_variants:
                learner_type = task_v['learner_type']
                learner_code = LEARNER_CODE[learner_type]
                corresponding_students = leaner_type_map[learner_code]
                task_map = set_task([task_v], students_ids=corresponding_students, tasks_map=task_map) # assigns corresponding learners task
    return task_map, 1


def save_tasks(task_map, students_folder):
    i = 0
    for student, tasks in task_map.items():
        student_folder = os.path.join(students_folder, student)
        for task in tasks:
            with open(f'{student_folder}/active_tasks/task{i}.json' , 'w+') as file:
                file.write(json.dumps(task))
            i += 1


def get_student_tasks(student_id):
    active_tasks_paths = os.path.join(STUDENTS_FOLDER, student_id, 'active_tasks')
    if not os.path.exists(active_tasks_paths):
        return [], -1
    task_filenames = glob.glob(active_tasks_paths + '/*')
    tasks = []
    for filename in task_filenames:
        with open(filename) as file:
            task = json.loads(file.read())
        tasks.append(task)
    return tasks, 1



# students_folder = 'students/grade 1/A'
# task_path = 'subjects/literature_4_2019/lesson1/tasks'
# task_map, res = distribute_tasks(tasks_path=task_path, students_path=students_folder)
# save_tasks(task_map, students_folder)