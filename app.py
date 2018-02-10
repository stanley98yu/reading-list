# app.py: Basic Flask program for running the reading list application.
# Author: Stanley Yu
# Date: 2/9/18
from flask import Flask, render_template, request
import requests


app = Flask(__name__)
app.config["DEBUG"] = True # Only include when testing app.

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/search", methods=["POST", "GET"])
def search():
	if request.method == "POST": # User used the search box.
		url = "https://www.googleapis.com/books/v1/volumes?q=" + request.form["user_search"]
		response_dict = requests.get(url).json()
		return render_template("results.html", api_data = response_dict)
	else:
		return render_template("search.html")

@app.route("/results")
def results():
	return render_template("results.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0")

