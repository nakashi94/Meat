from flask import Flask, render_template, request, session, redirect, url_for
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import ValidationError

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = b"random string..."

# global variables
member_data = {}

# UsersDataBase
db_uri = 'sqlite:///login.db'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

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

# Loginクラス定義
class LoginForm(FlaskForm):
    name = StringField('名前')
    mail = StringField('メールアドレス')
    submit = SubmitField('ログイン')

# EntryFormクラスの定義
class EntryForm(FlaskForm):
    name = StringField('名前')
    mail = StringField('メールアドレス')
    submit = SubmitField('アカウント作成')

    def validate_name(self, name):
        if User.query.filter_by(name=name.data).one_or_none():
            raise ValidationError('この名前はすでに使われています')

    def validate_mail(self, mail):
        if User.query.filter_by(mail=mail.data).one_or_none():
            raise ValidationError('このメールアドレスはすでに使われています')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# login page
@app.route('/testlogin', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if User.query.filter_by(name=form.name.data, mail=form.mail.data).one_or_none():
            user = User.query.filter_by(name=form.name.data).one_or_none()
            login_user(user)
            return redirect('/')
        else:
            return 'ログインに失敗しました'
    return render_template('testlogin.html',form=form)

# logout page
@app.route("/testlogout", methods=["GET"])
def logout():
    logout_user()
    return render_template('testlogout.html')

# sign up page
@app.route('/testentry', methods=['GET','POST'])
def entry():
  entry = EntryForm()
  if entry.validate_on_submit():
    newuser = User(name=entry.name.data, mail=entry.mail.data)
    db.session.add(newuser)
    db.session.commit()
    return redirect('/testlogin')
  return render_template('testentry.html', entry=entry)

# test用
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=80)
