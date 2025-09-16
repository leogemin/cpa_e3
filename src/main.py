from flask import Flask

APP_NAME: str = "CPA_RestAPI"

app = Flask(APP_NAME)

@app.route("/")
def hello_world():
  return "<p>Hello, World!</p>"