"""
Registration of a user 0 tokens
Each user gets 10 tokens
Store a sentence on our database for 1 token
Retrieve his stored sentence on out database for 1 token
"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db["Users"]

class Register(Resource):
    def post(self):
        #Step 1 get posted data by the user
        postedData = request.get_json()

        #Get the data
        username = postedData["username"]
        password = postedData["password"]

        hashed_pw = hashed = bcrypt.hashpw(password, bcrypt.gensalt())

        #Store username and password into the database
        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Sentence": "",
            "Tokens":6
        })

        retJson = {
            "status": 200,
            "msg": "You successfully signed up for the API."
        }
        return jsonify(retJson)

class Store(Resource):
    def post(self):
        #Step 1 get the posted data
        postedData = request.get_json()

        #Step 2 is to read the data
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        #Step 3 verify the username pw match
        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retJson = {
                "status": 302
            }
            return jsonify(retJson)
        #Step 4 verify user has enough Tokens
        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retJson = {
                "status": 301
            }
            return jsonify(retJson)
        #Step 5 store the sentence and return 200 OK
        users.update({
            "Username":username
            }, {
                "$set":{
                "Sentence":sentence,
                "Tokens":num_tokens-1
                }
            })

            retJson = {
                "status":200,
                "msg":"Sentence saved successfully"
            }
            return jsonify(retJson)

api.add_resource(Register, '/register')

if __name__=="__main__":
    app.run(host='0.0.0.0')
