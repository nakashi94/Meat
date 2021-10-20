from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = b"random string..."

name_list = {"hoge": "hogepiyo"}


@app.route("/", methods=["GET", "POST"])
def index():
    title = "Test"
    return render_template("index.html", title=title)


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=80)
