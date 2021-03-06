from importlib.resources import Resource
from flask import Flask,jsonify,request
from flask_restful import Api, Resource

from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.aNewDB
UserNum = db["UserNum"]

UserNum.insert_one({
    'num_of_users':0
})

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['num_of_users']
        new_num = prev_num + 1
        UserNum.update_one({}, {"$set":{"num_of_users":new_num}})
        return str("Hello user " + str(new_num))

def checkPostedData(postedData, functionName):
    if (functionName == "add" or functionName == "subtract" or functionName == "multiply"):
        if "x" not in postedData or "y" not in postedData:
            return 301 #Missing parameter
        else:
            return 200
    elif (functionName == "division"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif int(postedData["y"]) == 0:
            return 302
        else:
            return 200
class Add(Resource):
    def post(self):
        #If here then the resource was requested via POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Step 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "add")
        if (status_code!=200):
            retJson = {
                "Message":"An error happened",
                "Status code":status_code
            }
            return jsonify(retJson)

        #If here, then status code is 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Step 2: Add posted data
        ret = x+y
        retMap = {
            "Message": ret,
            "Status Code": 200
        }
        return jsonify(retMap)

class Subtract(Resource):
    def post(self):
        #If here then the resource was requested via POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Step 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "subtract")
        if (status_code!=200):
            retJson = {
                "Message":"An error happened",
                "Status code":status_code
            }
            return jsonify(retJson)

        #If here, then status code is 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Step 2: Subtract posted data
        ret = x-y
        retMap = {
            "Message": ret,
            "Status Code": 200
        }
        return jsonify(retMap)

class Multiply(Resource):
     def post(self):
        #If here then the resource was requested via POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Step 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "multiply")
        if (status_code!=200):
            retJson = {
                "Message":"An error happened",
                "Status code":status_code
            }
            return jsonify(retJson)

        #If here, then status code is 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Step 2: Multiply posted data
        ret = x*y
        retMap = {
            "Message": ret,
            "Status Code": 200
        }
        return jsonify(retMap)

class Divide(Resource):
    def post(self):
        #If here then the resource was requested via POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Step 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "division")
        if (status_code!=200):
            retJson = {
                "Message":"An error happened",
                "Status code":status_code
            }
            return jsonify(retJson)

        #If here, then status code is 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Step 2: Multiply posted data
        ret = (x*1.0)/y
        retMap = {
            "Message": ret,
            "Status Code": 200
        }
        return jsonify(retMap)

api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide,"/division")
api.add_resource(Visit, "/hello")


@app.route('/')
def hello_world():
    return "Hello world"

@app.route('/hithere')
def hi_there_everyone():
    return "I just hit /hithere"

@app.route('/add_two_nums', methods=["POST"])
def add_two_nums():
    #get x,y from the posted data
    dataDict = request.get_json()
     
    if "y" not in dataDict:
        return "ERROR", 305
    x = dataDict["x"]
    y = dataDict["y"]
    #add z=x+y
    z = x+y

    #prepare a JSON "z":z
    retJSON = { 
        "z":z    
    }

    #return jsonify
    return jsonify(retJSON), 200

@app.route('/bye')
def bye():
    #Prepare a response for the request that came to /bye
    age = 2*5
    #c = 1/0
    retJson = {
        'Name':'Elfarouk',
        'Age':age,
	"phones":[
            {
		"phoneName": "Iphone8",
		"phoneNumber": 11111
	    },
	    {
		"phoneName": "Nokia",
		"phoneNumber": 11121
	    }
	]
	
    }
    return jsonify(retJson)

if __name__=="__main__":
    app.run('0.0.0.0', debug=True)
