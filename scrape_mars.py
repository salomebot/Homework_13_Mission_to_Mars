# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import tweepy
import time
import pymongo

print("Scrape communication Active")

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    
    #NASA Mars News
    browser = init_browser()
    mars_dict = {}
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find('div', 'content_title', 'a')
     
    #print("NEWS TITLE & DESCRIPTION ACQUIRED")

    mars_dict["news_title"] = news_title.text

    news_text = soup.find('div', 'article_teaser_body')
    #print(news_text.text)
    
    mars_dict["news_text"] = news_text.text

    #JPL Mars Space Images - Featured Image

    browser = init_browser()
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.find("a",class_="button fancybox")["data-fancybox-href"]
    featured_image_url = "https://jpl.nasa.gov"+image
    mars_dict["featured_image_url"] = featured_image_url
    #print(featured_image_url)

    #Mars Weather
    # Twitter API Keys

    consumer_key = "vnn94VlkLW6ftf3umIyqvdkDc"
    consumer_secret = "0h6CnRFCa43h9yrXbe1zAB6vE9PVIRP1D6NO4lRweIBZNwCRay"
    access_token = "942946411133337600-TqcZS5K3pX1gznvkFFDKaotuEdhuafO"
    access_token_secret = "E3qQ5VBTuUc1uNmokmzm4CoUypjpRnCWp4RWTdVq2zUTs"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    user="@MarsWxReport"

    mars_tweet = api.user_timeline(user, count=1)
    mars_weather=mars_tweet[0]['text']
    mars_dict["mars_weather"] = mars_weather
    #print(mars_weather)

    #Mars Facts
    url3 = "https://space-facts.com/mars/"
    table_mars = pd.read_html(url3)
    df=table_mars[0]
    df.columns = ['Mars Facts', 'Measurements']
    time.sleep(5)
    html_table = df.to_html()
    html_table=html_table.replace('\n', '')
    mars_dict["table_html"] =  html_table

    #Mars Hemispheres
    browser = init_browser()
    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemi_title=[]
    title_hemi=soup.find_all("h3")
    for title in title_hemi:
        hemi_title.append(title.text.strip())
    #print(hemi_title)
    hemisphere_image_urls=[]

    for i in range(len(hemi_title)):
        time.sleep(5)
        title=hemi_title[i]
        image=browser.find_by_tag('h3')
        image[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        partial=soup.find("img", class_="wide-image")["src"]
        img_url='https://astrogeology.usgs.gov'  + partial
        dictionary={"title":title,"img_url":img_url}
        hemisphere_image_urls.append(dictionary)
        mars_dict["hemisphere_image_urls"] = hemisphere_image_urls   
        browser.quit()
    mars_dict["hemisphere_image_urls"] = hemisphere_image_urls   
    return mars_dict
