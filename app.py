from os import environ
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__=='__main__':
  HOST=environ.get('SERVER_HOST','localhost')
  try:
    PORT=int(environ.get('SERVER_PORT','5555'))
  except ValueError:
    PORT=5555
  app.run(HOST, PORT, debug=True)
  