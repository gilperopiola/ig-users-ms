import mysql.connector
import json
from flask import Flask, make_response, request
from flask_cors import CORS
import sys

app = Flask(__name__)
CORS(app)

@app.route("/save", methods=['POST'])
def save():

  print("New request!", file=sys.stderr)

  # connect to db
  db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ig_users"
  )

  cursor = db.cursor()

  # get body data
  body = request.data
  parsed = json.loads(body)

  id  = parsed['id']
  username  = parsed['username'] 
  fullName  = parsed['fullName']
  isPrivate = parsed['isPrivate']
  isVerified = parsed['isVerified']
  picId = parsed['picId']
  picUrl = parsed['picUrl']
  hasStory = parsed['hasStory']

  originUsername = parsed['originUsername'] # the username of the original account

  print("ID: " + str(id), file=sys.stderr)
  print("Username: " + str(username), file=sys.stderr)

  # check if exists
  userExists = False

  cursor.execute("SELECT * FROM users WHERE id = " + str(id) + " OR username = '" + str(username) + "'")
  results = cursor.fetchall()
  if len(results) > 0:
    print("ID: " + str(id) + " already exists!", file=sys.stderr)
    userExists = True

  # insert into db
  if not userExists:
    print("ID: " + str(id) + " does not exist!", file=sys.stderr)
    sql = "INSERT INTO users (id, username, fullName, isPrivate, isVerified, picId, picUrl, hasStory) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (str(id), username, fullName, isPrivate, isVerified, picId, picUrl, hasStory)
    cursor.execute(sql, val)
    db.commit()

  # check if exists on follows table
  userExists = False

  cursor.execute("SELECT * FROM follows WHERE username = '" + str(originUsername) + "' AND follows = '" + str(username) + "'")
  results = cursor.fetchall()
  if len(results) > 0:
    print("Follow relationship already exists!", file=sys.stderr)
    userExists = True

  # insert into follows table
  if not userExists:
    print("Follow relationship does not exist!", file=sys.stderr)
    sql = "INSERT INTO follows (username, follows) VALUES (%s, %s)"
    val = (originUsername, username)
    cursor.execute(sql, val)
    db.commit()

  response = make_response({}, 200)
  return response

if __name__ == '__main__':
    app.run(debug=True)
