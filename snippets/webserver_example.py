# http://flask.pocoo.org/docs/0.12/quickstart/

from flask import Flask
import time
app = Flask(__name__)


# pass url that should map to this function
@app.route('/')
def hello_world():
    # read arbitrary file
    with open('data.txt') as f:
        data = f.read()
    #     construct a string of output
    return """
    <p>
        Hello, World!
    </p>
    <p>
        The time is currently {}
    </p>
    <p>
        The contents of data.txt are: {}
    </p>
    """.format(time.ctime(), data)


if __name__ == '__main__':
    app.run(debug=True)
