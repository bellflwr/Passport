from flask import Flask, render_template  # type: ignore
import uuid
import json
import data

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")