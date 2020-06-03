from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/home")

@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/alien")
def alien():
    return render_template("alien.html")

@app.route("/human")
def human():
    return render_template("human.html")


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
