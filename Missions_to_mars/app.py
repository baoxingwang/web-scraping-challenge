from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
import pandas as pd
import pymongo
from pprint import pprint
from flask import Flask, render_template


url = 'https://mars.nasa.gov/news/'
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
browser.visit(url)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
news_title = soup.find('div', class_ = 'content_title').text
news_content = soup.find('div', class_ = 'article_teaser_body').text


conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.marsDB

collection = db.data

docs = [{
    'news_title': news_title

},
  {
      'news_content': news_content
  }      
]

collection.insert_many(docs)


db.roster.drop()
app = Flask(__name__)

@app.route('/')
def index():
    # Store the entire team collection in a list
    mars_dict = {"news_t": "news_title",
                 "news_c": "news_content"

    }


    # Return the template with the players list passed in
    return render_template('index.html', dict=mars_dict)

if __name__ == "__main__":
    app.run(debug=True)
