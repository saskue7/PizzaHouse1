from unicodedata import name
from flask import Flask
from flask_restful import Resource,Api,reqparse,abort
from flask_pymongo import PyMongo



app = Flask(__name__)
api = Api(app)


app.config["MONGO_URI"]="mongodb+srv://Saskue:Saskue@cluster0.9hoqgvh.mongodb.net/pizza_house"
client = PyMongo(app)
db = client.db

data = db.orders.find()
p = list(data)


task_post_args = reqparse.RequestParser()
task_post_args.add_argument("order",action='append',required=True,help="Have to put as order suggest")

class Welcome(Resource):
 def get(self):
  return "Welcome to Pizza House"

class Get(Resource):
 def get(self):
  d={}
  for i in p:
   d[i["_id"]]={"order":i["order"]}
  return d 
class Order(Resource):
 def get(self,order_id):
  for i in p:
   if  i['_id']==order_id:
    return {"order":i["order"]}

 def post(self,order_id):
  args = task_post_args.parse_args()
  for i in p:
   if i["_id"]==order_id:
    abort(409,message="Already Exists")
 
  db.orders.insert_one({"_id":order_id,"order":args["order"]})
  p.append({"_id":order_id,"order":args["order"]})
  return {"order":args["order"]}     


api.add_resource(Get,'/getorders')
api.add_resource(Order,'/getorders/<int:order_id>')
api.add_resource(Welcome,'/welcome')

if __name__=="__main__":
 app.run(debug=True)
