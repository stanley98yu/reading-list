from flask import Flask


app = Flask(__name__)
app.config["DEBUG"] = True # Only include when testing app.

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/search/<query>")
def search(query):
    return query

if __name__ == "__main__":
    app.run(host="0.0.0.0")

