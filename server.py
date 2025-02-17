from flask import Flask
from flask_session import Session

server = Flask(__name__)
server.config['SECRET_KEY'] = 'cbe2e8e1c261e8cc217a3fe1850e3c09838b68755af7995d'
server.config['SESSION_TYPE'] = 'filesystem'

Session(server)
