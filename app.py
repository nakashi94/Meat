from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = b"random string..."

name_list = {"hoge": "hogepiyo"}


@app.route("/", methods=["GET", "POST"])
def index():
    title = "home"
    return render_template(
        "index.html", title=title
    )  # login.htmlをindex.html(アプリのホーム画面)に変える


@app.route("/login", methods=["GET", "POST"])
def login():
    title = "Login"
    return render_template("login.html", title=title)


@app.route("/registerAccount", methods=["GET", "POST"])
def register():
    title = "RegisterAccount-form"
    return render_template("registerAccount.html", title=title)


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


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=80)
