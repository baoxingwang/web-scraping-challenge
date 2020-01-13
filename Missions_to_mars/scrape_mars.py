from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info ():
    browser = init_browser()
    #find the news title and content
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find('div', class_ = 'content_title').text
    news_content = soup.find('div', class_ = 'article_teaser_body').text

    # find the feature image link 

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    # browser.click_link_by_partial_text('FULL ')
    html = browser.html
    soup = bs(html, 'html.parser')
    fancybox = soup.find_all('a', class_='fancybox')[0]
    fea_img = fancybox.get('data-fancybox-href')
    fea_img=(f'https://www.jpl.nasa.gov{fea_img}')



    #find the weather info
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    weather = soup.find('p', class_ = 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    weather = weather[0:-26]

    # find the fact table"
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['','values']
    table = df.to_html()

    # find hemisphere images inks 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('Cerberus ')
    html = browser.html
    soup = bs(html, 'html.parser')
    hem_img_1 = soup.find('a', target = '_blank')["href"].strip('')

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('Schiaparelli ')
    html = browser.html
    soup = bs(html, 'html.parser')
    hem_img_2 = soup.find('a', target = '_blank')["href"].strip('')

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('Syrtis ')
    html = browser.html
    soup = bs(html, 'html.parser')
    hem_img_3 = soup.find('a', target = '_blank')["href"].strip('')

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('Valles ')
    html = browser.html
    soup = bs(html, 'html.parser')
    hem_img_4 = soup.find('a', target = '_blank')["href"].strip('')


    #collect all data into mars_dict 
    mars_dict = {
        "n_t" : news_title,
        "n_c" : news_content,
        "f_i": fea_img,
        "wea" : weather,
        "ta" : table,
        "h_i_1": hem_img_1,
        "h_i_2": hem_img_2,
        "h_i_3": hem_img_3,
        "h_i_4": hem_img_4
    }

# Close the browser after scraping
    browser.quit()

    # Return results
    return mars_dict

