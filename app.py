# import module
from flask import Flask, render_template
from flask import Response, request, redirect, session, url_for
from flask import send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError


# flask instance
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = b"random string..."

# global variables
member_data = {}

# UsersDataBase
db_uri = 'sqlite:///login.db'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

#データベース作成
# Userクラス定義
class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    mail = db.Column(db.Text())
    def __init__(self, name, mail):
        self.name = name
        self.mail = mail

db.create_all()

# Teamsクラス定義
class Teams(db.Model):
    team_id = db.Column(db.Integer, primary_key=True)
    teamname = db.Column(db.String(50), nullable=False)    

# Messageクラス定義
class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    teamname = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    today_do = db.Column(db.String(64), nullable=False)
    tomorrow_do = db.Column(db.String(64), nullable=False)
    importance = db.Column(db.Integer, nullable=False)

# Messageクラス定義
class Progress(db.Model):
    feel_id = db.Column(db.Integer, primary_key=True)
    teamname = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    progress = db.Column(db.String(64), nullable=False)
    feel = db.Column(db.Integer, nullable=False)

# Loginクラス定義
class LoginForm(FlaskForm):
    name = StringField('username')
    mail = StringField('mailaddress')
    submit = SubmitField('Login')

# EntryFormクラスの定義
class EntryForm(FlaskForm):
    name = StringField('username')
    mail = StringField('mailaddress')
    submit = SubmitField('Sign up')

    def validate_name(self, name):
        if User.query.filter_by(name=name.data).one_or_none():
            raise ValidationError('この名前はすでに使われています')

    def validate_mail(self, mail):
        if User.query.filter_by(mail=mail.data).one_or_none():
            raise ValidationError('このメールアドレスはすでに使われています')

#--------------------------------------------------------------------------------------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#--------------------------------------------------------------------------------------
#機能実装

# login page
@app.route('/login', methods=['GET','POST'])
def logina():
    title = "Login"
    form = LoginForm()
    if form.validate_on_submit():
        if User.query.filter_by(name=form.name.data, mail=form.mail.data).one_or_none():
            user = User.query.filter_by(name=form.name.data).one_or_none()
            login_user(user)
            items = Teams.query.all()
            return render_template('teamlist.html',user=user, items=items)
        else:
            return 'ログインに失敗しました'
    return render_template('login.html', title=title, form=form)

# logout page
@app.route("/testlogout", methods=["GET"])
def logout():
    logout_user()
    return render_template('testlogout.html')



# @app.route("/registerAccount", methods=["GET", "POST"])
# def register():
    # title = "RegisterAccount-form"
    # return render_template("registerAccount.html", title=title)




# sign up page
@app.route('/registerAccount', methods=['GET','POST'])
def entry():
    title = "RegisterAccount-form"
    entry = EntryForm()
    if entry.validate_on_submit():
        newuser = User(name=entry.name.data, mail=entry.mail.data)
        db.session.add(newuser)
        db.session.commit()
        return redirect('/login')
    return render_template('registerAccount.html', title=title, entry=entry)

@app.route('/fromteam', methods=['Get', 'POST'])
def fromteam():
    items = Teams.query.all()
    u = request.form.get('username')
    user = User.query.filter_by(name=u).first()
    return render_template('teamlist.html', items=items, user=user)

@app.route('/teamlist', methods=['Get', 'POST'])
def teamlist():
    if request.method == 'GET':
        items = Teams.query.all()
        u = request.form.get('user')
        return render_template('teamlist.html', items=items, u=u)
    else:
        u = request.form.get('user')
        return render_template('teamform.html', u=u)

#チーム作成
@app.route('/teamform', methods=['Get', 'POST'])
def teamform():
    u = request.form.get('username')
    t = request.form.get('teamname')
    return render_template('teamregister.html', t=t, u=u)

#チーム登録確認
#データベース格納
@app.route('/teamregister', methods=['GET', 'POST'])
def teamregister():
    t = request.form.get('teamname')
    item = Teams(teamname=t)
    db.session.add(item)
    db.session.commit()
    d = datetime.now()
    d = d.strftime('%Y:%m:%d %H:%M:%S')
    items = Teams.query.all()
    u = request.form.get('username')
    user = User.query.filter_by(name=u).first()
    return render_template('teamlist.html', items=items, user=user)

#各チーム画面に遷移
@app.route('/toteam', methods=['GET', 'POST'])
def toteam():
    t = request.form.get('team')
    username = request.form.get('user')
    progress = Progress.query.filter_by(teamname=t).all()
    items = Message.query.filter_by(teamname=t).all()
    return render_template('home.html', t=t, u=username, items=items, progresses=progress)

@app.route('/team', methods=['Get', 'POST'])
def layout():
    t = request.form.get('team')
    u = request.form.get('username')
    return render_template('form.html', t=t, u=u)

#データ入力----------------------------------------------------------------------------

#日報作成
@app.route('/dayform', methods=['GET', 'POST'])
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
@app.route('/dayregister', methods=['GET', 'POST'])
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
        d = d.strftime('%Y:%m:%d %H:%M:%S')
        #チーム一覧ページ移動

        progress = Progress.query.filter_by(teamname=t).all()
        items = Message.query.filter_by(teamname=t).all()
        return render_template('home.html', t=t, u=u, items=items, progresses=progress)


#進捗
@app.route('/prog', methods=['Get', 'POST'])
def proglayout():
    t = request.form.get('team')
    u = request.form.get('username')
    return render_template('progform.html', t=t, u=u)

#進捗作成
@app.route('/progform', methods=['GET', 'POST'])
def progforms():
    t = request.form.get('team')
    u = request.form.get('user_id')
    a = request.form.get('progress')
    b = request.form.get('feel')
    if b == "１":
        b = "順調"
    elif b == "２":
        b = "予定通り"
    elif b == "３":
        b = "ギリギリ"
    elif b == "４":
        b = "少し遅れてる"
    elif b == "５":
        b = "やばい"
    return render_template('progregister.html', t=t, u=u, a=a, b=b)

#進捗登録確認
#データベース格納
@app.route('/progregister', methods=['GET', 'POST'])
def progresister():
    t = request.form.get('team')
    u = request.form.get('user_id')
    a = request.form.get('progress')
    b = request.form.get('feel')
    item = Progress(teamname = t, user_id=u, progress=a, feel=b)
    db.session.add(item)
    db.session.commit()
    c = datetime.now()
    c = c.strftime('%Y:%m:%d %H:%M:%S')
    #一覧ページ移動
    progress = Progress.query.filter_by(teamname=t).all()
    items = Message.query.filter_by(teamname=t).all()
    return render_template('home.html', t=t, u=u, items=items, progresses=progress)







# ホームページ
@app.route("/", methods=["GET", "POST"])
def index():
    title = "home"
    return render_template(
        "index.html", title=title
    )  # login.htmlをindex.html(アプリのホーム画面)に変える




@app.route("/Team", methods=["GET", "POST"])
def registerTeam():
    title = "Team-form"
    return render_template("Team.html", title=title)


@app.route("/list-form", methods=["GET", "POST"])
def list():
    title = "list-form"
    return render_template("list-form.html", title=title)


@app.route("/progressform", methods=["GET", "POST"])
def progform():
    title="進捗状況"
    return render_template("progressform.html",title=title)


@app.route("/reportform", methods=["GET", "POST"])
def input():
    title="日報"
    return render_template("reportform.html",title=title)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
