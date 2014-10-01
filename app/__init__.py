from flask.ext.api import FlaskAPI
import couchdb

server = couchdb.Server()

update = False

try:
    db = server['peleton-db']
except:
    db = server.create('peleton-db')
    update = True

if update:
    db.update([{"_id": "A", "list": [2, 3, 8], "idx": 0}, {"_id": "B", "list": [4, 5, 6], "idx": 0}])
    db.update([{"_id": "merge"}])

app = FlaskAPI(__name__)

from app import routes

from routes import quiz

app.register_blueprint(quiz)