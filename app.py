from flask import Flask, render_template
import requests


app = Flask(__name__)
app.config["DEBUG"] = True # Only include when testing app.

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/search")
def search():
    return render_template("search.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0")

