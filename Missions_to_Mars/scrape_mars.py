#!/usr/bin/env python
# coding: utf-8

# ## Web Scraping Homework - Mission to Mars ##

from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import pandas as pd

def scrape():

    nasa_url = "https://mars.nasa.gov/news/"
    spaceimages_url = "https://spaceimages-mars.com/"
    marsfacts_url = "https://galaxyfacts-mars.com/"
    hemispheres_url = "https://marshemispheres.com/"

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

# ### NASA Mars News ###

    browser.visit(nasa_url)

    nasa_html = browser.html
    nasa_soup = bs(nasa_html, "html.parser")

    news_title =  nasa_soup.find_all("div", class_="content_title")[1].text
    news_p = nasa_soup.find_all("div", class_="article_teaser_body")[1].text

    print("* Latest News Title *")
    print(news_title)
    print()
    print("* Paragraph Text *")
    print(news_p)

# ### JPL Mars Space Images - Featured Image ###

    browser.visit(spaceimages_url)

    space_html = browser.html
    space_soup = bs(space_html, "html.parser")

    button = browser.find_by_tag('button')[1]
    button.click()

    img_html = browser.html
    img_soup = bs(img_html, "html.parser")

    img_url = img_soup.find('img', class_='fancybox-image').get('src')
    featured_image_url = spaceimages_url + img_url
    print(featured_image_url)

# ### Mars Facts ###

    marsfacts_url = "https://galaxyfacts-mars.com/"
    browser.visit(marsfacts_url)
    html_df = pd.read_html(marsfacts_url, header=0)
    html_df = html_df[0]
    print(html_df)
    facts_html = html_df.to_html()
    print(facts_html)

# ### Mars Hemispheres ###
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    hemispheres_soup = bs(hemispheres_html, "html.parser")
    list_urls = hemispheres_soup.find_all('a', class_="itemLink product-item")
    list_urls
    links_list = []

    for x in list_urls:
        if (x["href"] != "#"):
            img_url = hemispheres_url + x["href"]
        if img_url not in links_list:
            links_list.append(img_url)
    
    links_list

    combined_url = []

    for x in links_list:
        browser.visit(x)
        links_html = browser.html
        links_soup = bs(links_html, 'html.parser')
        title_links = links_soup.find_all("h2", class_="title")[0].text.split()
        title_links.pop()
        title_links = " ".join(title_links)
        image_url = hemispheres_url + links_soup.find_all('img', class_="wide-image")[0]["src"]
        list_dict = {"title": title_links, "img_url": image_url}
        combined_url.append(list_dict)
    
    combined_url

    return



