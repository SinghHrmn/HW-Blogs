from flask import Flask

from .settings import DEBUG, PORT

app = Flask(__name__)

from . import routes


def run(port=PORT, debug=DEBUG):
    app.run(port=port, debug=True)
