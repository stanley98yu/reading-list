# app.py: Basic Flask program for running the reading list application.
# Author: Stanley Yu
# Date: 2/9/18
from flask import Flask, render_template, request, redirect
from flask.ext.mongoengine import MongoEngine
from flask.ext.mongoengine.wtf import model_form
from flask.ext.login import LoginManager, login_user, logout_user
from wtforms import PasswordField
import requests

app = Flask(__name__)
app.config["DEBUG"] = True  # Only include when testing app.
app.config['MONGODB_SETTINGS'] = {'db':'books'}
'''
app.config['SECRET_KEY'] = 'fe6b7c63'
app.config['WTF_CSRF_ENABLED'] = True
login_manager = LoginManager()
login_manager.init_app(app)
'''
# Database model for favorite books.
db = MongoEngine(app)
class FavoriteBook(db.Document):
    author = db.StringField(required=True)
    title = db.StringField(required=True)
    link = db.StringField(required=True)

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Search page
@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":  # User used the search box.
        url = "https://www.googleapis.com/books/v1/volumes?q=" + request.form["user_search"]
        response_dict = requests.get(url).json()
        return render_template("results.html", api_data=response_dict)
    else:
        return render_template("search.html")


# Results page
@app.route("/results")
def results():
    return render_template("results.html")

# Favorite function
@app.route("/favorite/<id>")
def fav(id):
    book_url = "https://www.googleapis.com/books/v1/volumes/" + id
    book_dict = requests.get(book_url).json()
    new_fav = FavoriteBook(
        author=book_dict["volumeInfo"]["authors"][0],
        title=book_dict["volumeInfo"]["title"],
        link=book_url)
    new_fav.save()
    return render_template("confirm.html", api_data=book_dict)

# Favorites viewing page
@app.route("/favorites")
def favorite():
    favorites = FavoriteBook.objects()
    return render_template("favorites.html", favorites=favorites)
'''
# Registration page
@app.route("/register", methods=["POST", "GET"])
def register():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        form.save()
        return redirect("/login")
    return render_template("register.html", form=form)

# Login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(name=form.name.data, password=form.password.data)
        login_user(user)
        return redirect('/search')
    return render_template('login.html', form=form)

# Logout page
@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

# User class for logins.
class User(db.Document):
    name = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)

    def is_authenticated(self):
        users = User.objects(name=self.name, password=self.password)
        return len(users) != 0

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.name

# User login forms.
UserForm = model_form(User)
UserForm.password = PasswordField('password')

# Load users.
@login_manager.user_loader
def load_user(name):
    users = User.objects(name=name)
    if len(users) != 0:
        return users[0]
    else:
        return None
'''
if __name__ == "__main__":
    app.run(host="0.0.0.0")
