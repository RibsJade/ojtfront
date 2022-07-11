from flask import Flask, jsonify, request, Response, render_template, url_for, redirect
from werkzeug.utils import secure_filename
import os
import shutil
import requests
import datetime
import json
import csv
import sys
from pathlib import Path


import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)


def saveFile(directory, file):

    filepath = os.path.join(directory, file.filename)

    print(filepath, file=sys.stderr)
    if os.path.exists(filepath):
        os.remove(filepath)
    file.save(filepath)
    return "saved"


@app.route('/filetest', methods=['POST'])
def filehandling():
    if request.method == 'POST':
        directory = request.form.get("username")

        errors = []
        if directory != "":
            directory = os.path.join("users", directory)
            if os.path.isdir(directory):
                shutil.rmtree(directory)
            os.mkdir(directory)

            if 'file1' in request.files:  # wala na ni
                file = request.files['file1']  # as is
                if file.filename != '':  # functuion
                    __, fileext = os.path.splitext(file.filename)
                    allowed = ['.csv']
                    if fileext.lower() in allowed:
                        saveFile(directory, file)
                    else:
                        errors.append('file1 extension must be csv')
                else:
                    errors.append('file1 name is empty')
            else:
                errors.append('file1 not found')

            if 'file2' in request.files:
                file = request.files['file2']
                if file.filename != '':
                    __, fileext = os.path.splitext(file.filename)
                    print(fileext.lower(), file=sys.stderr)
                    allowed = ['.xls', '.xlsx']
                    if fileext.lower() in allowed:
                        saveFile(directory, file)
                    else:
                        errors.append('file2 extension must be xls or xlsx')
                else:
                    errors.append('file1 name is empty')
            else:
                errors.append('file1 not found')
        else:
            errors.append('directory must not be blank')
        if not errors:
            return jsonify('file uploaded successfully')
        else:
            return jsonify(errors)
    else:
        return jsonify('hello')
    # filepath = os.path.join(directory, filename)
    # mylist = []
    # if not os.path.exists(filepath):
    #     data = open(filepath, "w")
    #     data.close()
    # with open(filepath) as file:
    #     data = csv.reader(file, delimiter='\t')
    #     for row in data:
    #         mylist.append(row)

    # return jsonify(mylist)


# while(True):
#     response = requests.get("http://worldtimeapi.org/api/timezone/Asia/Manila")
#     data = response.json()
#     datetimeutc = data['datetime']

#     dtime = datetimeutc
#     date_time_obj = datetime.datetime.strptime(dtime, '%Y-%m-%dT%H:%M:%S.%f%z')

#     if date_time_obj.time() == datetime.time(0, 0, 0):
#         if os.path.isdir('users'):
#             shutil.rmtree('users')
#             os.mkdir('users')


if __name__ == "__main__":
    app.run(debug=True)
