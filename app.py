# app.py: Basic Flask program for running the reading list application.
# Author: Stanley Yu
# Date: 2/9/18
from flask import Flask, render_template, request
from flask.ext.mongoengine import MongoEngine
import requests


app = Flask(__name__)
app.config["DEBUG"] = True # Only include when testing app.
app.config['MONGODB_SETTINGS'] = { 'db' : 'books' }

# Home page
@app.route("/")
def hello():
    return render_template("index.html")

# Search page
@app.route("/search", methods=["POST", "GET"])
def search():
	if request.method == "POST": # User used the search box.
		url = "https://www.googleapis.com/books/v1/volumes?q=" + request.form["user_search"]
		response_dict = requests.get(url).json()
		return render_template("results.html", api_data = response_dict)
	else:
		return render_template("search.html")

# Results page
@app.route("/results")
def results():
	return render_template("results.html")

# Database model for favorite books.
db = MongoEngine(app)
class FavoriteBook(db.Document):
	author = db.StringField(required=True)
	title = db.StringField(required=True)
	link = db.StringField(required=True)

# Favorite function
@app.route("/favorite/<id>")
def favorite(id):
	book_url = "https://www.googleapis.com/books/v1/volumes/" + id
	book_dict = requests.get(book_url).json()
	new_fav = FavoriteBook(
		author=book_dict["volumeInfo"]["authors"][0], 
		title=book_dict["volumeInfo"]["title"], 
		link=book_url
	)
	new_fav.save()
	return render_template("confirm.html", api_data=book_dict)

# Favorites viewing page
@app.route("/favorites")
def favorites():
	favorites = FavoriteBook.objects()
	return render_template("favorites.html", favorites=favorites)

if __name__ == "__main__":
    app.run(host="0.0.0.0")

