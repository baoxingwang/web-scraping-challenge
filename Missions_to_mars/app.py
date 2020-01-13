from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
# mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

# Define the collection and drop any existing data for this exercise
a = mongo.db.mars_data
a.drop()

# route visit the index page
@app.route("/")
def home():

    # Find one record of data from the mongo database
    x = a.find_one()

    # Return template and data
    return render_template("index.html", web =x)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_dict = scrape_mars.scrape_info()

    # Insert the results into the database
    a.insert_one(mars_dict)
    # The option below would update the existing record (or insert)
    # costaRica_data.update({}, costa_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)