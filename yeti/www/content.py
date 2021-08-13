from yeti import app
import logging
logger = logging.getLogger(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"