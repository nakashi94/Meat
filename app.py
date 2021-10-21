# import module
from flask import Flask, render_template
from flask import Response, request, redirect, url_for
from flask import send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date


# flask incetance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

#データベース作成
class Teams(db.Model):
    team_id = db.Column(db.Integer, primary_key=True)
    teamname = db.Column(db.String(50), nullable=False)    

class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    teamname = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    today_do = db.Column(db.String(64), nullable=False)
    tomorrow_do = db.Column(db.String(64), nullable=False)
    importance = db.Column(db.Integer, nullable=False)


@app.route('/', methods=['Get', 'POST'])
def teamlist():
    #if request.method == 'GET':
    #    return render_template('index.html')
    if request.method == 'GET':
        items = Teams.query.all()
        return render_template('teamlist.html', items=items)
    else:
        #u = request.form.get('user_id')
        return render_template('teamform.html')

#チーム作成
@app.route('/teamform', methods=['Get', 'POST'])
def teamform():
    if request.method == 'GET':
        #u = request.form.get('user_id')
        return render_template('teamform.html')
    else:
        t = request.form.get('teamname')
        return render_template('teamregister.html', t=t)

#チーム登録確認
#データベース格納
@app.route('/teamregister', methods=['GET', 'POST'])
def teamregister():
    if request.method == 'GET':
        return render_template('teamsub.html')
    else:
        t = request.form.get('teamname')
        item = Teams(teamname=t)
        db.session.add(item)
        db.session.commit()
        d = datetime.now()
        #d = d.strftime('%Y年%m月%d日 %H:%M:%S')
        return render_template('teamsub.html', d=d)

#登録完了
@app.route('/teamsub', methods=['GET', 'POST'])
def teamsub():
    if request.method == 'GET':
        return render_template('teamsub.html')
    else:
        items = Teams.query.all()
        return render_template('teamlist.html', items=items)

#各チーム画面に遷移
@app.route('/toteam', methods=['GET', 'POST'])
def toteam():
    t = request.form.get('team')
    user_id = 'test'
    #items = Message.query.all()
    items = Message.query.filter_by(teamname=t).all()
    return render_template('home.html', t=t, u=user_id, items=items)

@app.route('/team', methods=['Get', 'POST'])
def layout():
    t = request.form.get('team')
    u = request.form.get('user_id')
    return render_template('form.html', t=t, u=u)

#日報作成
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        t = request.form.get('team')
        u = request.form.get('user_id')
        return render_template('form.html', t=t, u=u)
    else:
        t = request.form.get('team')
        u = request.form.get('user_id')
        a = request.form.get('done')
        b = request.form.get('do')
        c = request.form.get('importance')
        return render_template('register.html', t=t, u=u, a=a, b=b, c=c)

#日報登録確認
#データベース格納
@app.route('/register', methods=['GET', 'POST'])
def resister():
    if request.method == 'GET':
        return render_template('sub.html')
    else:
        t = request.form.get('team')
        u = request.form.get('user_id')
        a = request.form.get('done')
        b = request.form.get('do')
        c = request.form.get('importance')
        d = datetime.now()
        item = Message(teamname = t, user_id=u, today_do=a, tomorrow_do=b, importance=c)
        db.session.add(item)
        db.session.commit()
        #d = d.strftime('%Y年%m月%d日 %H:%M:%S')
        return render_template('sub.html', t=t, d=d)

#日報登録完了
@app.route('/sub', methods=['GET', 'POST'])
def sub():
    if request.method == 'GET':
        return render_template('sub.html')
    else:
        items = Message.query.all()
        team = request.form.get('team')
        user_id = 'test'
        return render_template('home.html', t=team, u=user_id, items=items)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)