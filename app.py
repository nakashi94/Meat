# import module
from flask import Flask, render_template
from flask import Response, request, redirect, url_for
from flask import send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)

@app.route('/', methods=['Get', 'POST'])
def index():
    if request.method == 'GET':
    #return "test"
        return render_template('home.html')
    else:
        return render_template('form.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        a = request.form.get('done')
        b = request.form.get('do')

        return render_template('register.html', a=a, b=b)

#データベース格納
@app.route('/register', methods=['GET', 'POST'])
def resister():
    if request.method == 'GET':
        return render_template('sub.html')
    else:
        return render_template('sub.html')

@app.route('/sub', methods=['GET', 'POST'])
def sub():
    if request.method == 'GET':
        return render_template('sub.html')
    else:
        return render_template('home.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)