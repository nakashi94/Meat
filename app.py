from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = b"random string..."

name_list = {"hoge": "hogepiyo"}


@app.route("/", methods=["GET", "POST"])
def index():
    title = "home"
    return render_template(
        "login.html", title=title
    )  # login.htmlをindex.html(アプリのホーム画面)に変える


@app.route("/login", methods=["GET", "POST"])
def login():
    title = "Login"
    return render_template("login.html", title=title)


@app.route("/register", methods=["GET", "POST"])
def register():
    title = "Register-form"
    return render_template("register.html", title=title)


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=80)
