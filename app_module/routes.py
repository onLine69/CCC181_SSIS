from flask import render_template
from . import app

# The Homepage
@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')