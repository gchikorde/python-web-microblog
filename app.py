import datetime
import os
from flask import Flask,render_template,request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv() #while deployment check for env variable in .env file

def create_app(): #flask app factory pattern, to prevent creation of multiple instances of MongoClient
    app = Flask(__name__)

    #uri = "mongodb+srv://gchikorde:Pratibha210@microblog-application.huwsf.mongodb.net/?retryWrites=true&w=majority&appName=microblog-application"
    #uri = "mongodb+srv://gchikorde:Pratibha210@mycluster.huwsf.mongodb.net/"

    ## Create a new client and connect to the server
    #client = MongoClient(uri, server_api=ServerApi('1'))
    #client = MongoClient(os.getenv("MONGODB_URI"))
    
    #app.db= client.microblog

    entries = []

    @app.route("/connect/") #for testing connection but timeout issue is there
    def connection():

        uri = "mongodb+srv://gchikorde:Pratibha210@microblog-application.huwsf.mongodb.net/?retryWrites=true&w=majority&appName=microblog-application"

        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))

        app.db= client.microblog

        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    @app.route("/", methods=["GET", "POST"])
    def home():
        #print([e for e in app.db.entries.find({})]) #list comprehension

        if request.method=="POST":
            entry_content=request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            entries.append((entry_content, formatted_date))
            #app.db.entries.insert({"content":entry_content, "date":formatted_date})

        entries_with_date=[
            (
                entry[0],
                entry[1],
                datetime.datetime.strptime(entry[1], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in entries
        ] #this is temporary collection

        # entries_with_date=[
        #     (
        #         entry["content"],
        #         entry["date"],
        #         datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
        #     )
        #     for entry in app.db.entries.find({}) #this is from DB
        # ]
        return render_template("home.html",entries=entries_with_date)
        
    return app