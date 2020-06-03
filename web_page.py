from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/")
def index():
    """
    First main page.
    """
    return render_template("index.html")


@app.route("/alien", methods=["POST"])
def alien():
    """
    Page with dictionary.
    """
    
    return render_template("created_dict.html")

@app.route("/human", methods=["POST"])
def human():
    """
    Page with dictionary.
    """
    
    return render_template("created_dict.html")


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
