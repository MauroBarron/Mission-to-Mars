##
## app.py Module 10.5.1 Use Flask to Create a Web App
##

## Dependencies
# use Flask to render a template
from flask import Flask, render_template
# use PyMongo to engage our Mongo db
from flask_pymongo import PyMongo
# import the scraping.py script created for pulling Mars data.
import scraping

## Set up Flask:
app = Flask(__name__)

## Use flask_pymongo to setup a mongo connection
# app will connect to Mongo using a URI = local host mongo db mars_app 
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# call an instance of Mongo using Flask's PyMongo
mongo = PyMongo(app)

## Set Up App Routes using Flask

#Home page
@app.route("/")
# define index function 
def index():
   mars=mongo.db.mars.find_one() #Use the mongo mars db. Created via command line: use mars_app
    # tells Flask to return HTML template using index.html
    # tells Python to use the "mars" collection in the MongoDB
    ##!! Essentially: Flask: use index.html template to return Python call to Mongo db mars
   return render_template("index.html", mars=mars)
   

## Scraping Route
# define Flask route, /scrape with will run our function
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars 
   mars_data = scraping.scrape_all() 
   mars.update({}, mars_data, upsert=True) 
   return "Scraping Successful!"

if __name__ == "__main__":
   app.run()