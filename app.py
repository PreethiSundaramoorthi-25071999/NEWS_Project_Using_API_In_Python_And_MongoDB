from flask import Flask, render_template,request,redirect,url_for,session
from newsapi import NewsApiClient
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
mongo_url="mongodb://localhost:27017"
mongo_var=MongoClient(mongo_url)
db=mongo_var.NEWS_project
collection=db.login_details
api_key = "2c7c5cae1b334f37b64d5011c7bc8978" 
app.secret_key="key"

newsapi = NewsApiClient(api_key=api_key)

@app.route('/',methods=["POST","GET"])
def home():
    if request.method=="POST":
        Name=request.form.get("Name")
        Password=request.form.get("Password")
        data_url=collection.find_one({"Name":Name,"Password":Password})
        if data_url:
         if Name==data_url["Name"] and Password==data_url["Password"]:
            session['Name']=Name
            return redirect(url_for("index"))
         else:
            return "Invalid Credentials"
    return render_template("login.html")
    
@app.route('/newuser',methods=["POST","GET"])
def newuser():
    if request.method=="POST":
     Name=request.form.get("Name")
     Password=request.form.get("Password")
     dict1={}
     dict1.update({"Name":Name})
     dict1.update({"Password":Password})
     collection.insert_one(dict1)
     return redirect(url_for("index"))
    return render_template("newuser.html")

@app.route("/logout")
def logout():
    session.pop("Name",None)
    return redirect(url_for("home"))

@app.route('/home')
def index():
    top_headlines = newsapi.get_top_headlines(country='in', language='en', page_size=5)
    articles = top_headlines['articles']
    return render_template('home.html', articles=articles)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        search_results = newsapi.get_everything(q=query, language='en', page_size=5)
        articles = search_results['articles']
    else:
        articles = []
    return render_template('home.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
