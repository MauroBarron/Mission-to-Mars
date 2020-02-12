# Beautiful Soup, Splinter, Pandas and Mission to Mars

# Dependencies
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
#import requests as re

## Our Magical scraping all function:
def scrape_all():
    # Initiate headless driver for deployment. don't have to be headless
    browser = Browser("chrome", executable_path="chromedriver", headless=True) 
    # New Variables in Function
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data= {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres(browser)
        }
    browser.quit()
    return data

## Set the executable path and initialize the chrome browser in splinter

## browser = Browser("chrome", executable_path="chromedriver", headless=True) 
    
### Scraping the Mars NASA news site
def mars_news(browser):
    ##set FLASK Splinter Browser
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Parse with BeautifulSoup and create a new element.
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    try:  ## Get data
        # set the parent elements
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use a parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_paragraph = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_paragraph

## Featured Image :Scraping the JPL NASA Featured Image
def featured_image(browser):
    # Set the Splinter Browser
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # get data
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
        return None    
    
    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    # close the function returning img_url.
    return img_url

## Scrape Mars Data
## https://space-facts.com/mars/
def mars_facts():
    try:
    # Use Pandas 'read_html' to scrape facts table into a data frame 
        df = pd.read_html('http://space-facts.com/mars/')[0]  # [0] pulls only first table
    except BaseException:
        return None
    #define columns
    df.columns=['Description', 'Data']
    df.set_index('Description', inplace=True)

    # Extract to html
    return df.to_html()
# paste below here
if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
#  Get Hemisphere Image and link. 
def hemispheres(browser):
    # A way to break up long strings
    url = (
        "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    )
    browser.visit(url)
    # Click the link, find the sample anchor, return the href
    hemisphere_image_urls = []
    for i in range(4):
        # Find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item h3")[i].click()
        hemi_data = scrape_hemisphere(browser.html)
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemi_data)
        # Finally, we navigate backwards
        browser.back()
    return hemisphere_image_urls

def scrape_hemisphere(html_text):
    # parse html text
    hemi_soup = soup(html_text, "html.parser")
    # adding try/except for error handling
    try:
        title_elem = hemi_soup.find("h2", class_="title").get_text()
        sample_elem = hemi_soup.find("a", text="Sample").get("href")
    except AttributeError:
        # Image error will return None, for better front-end handling
        title_elem = None
        sample_elem = None
        
    hemispheres = {"title": title_elem, "img_url": sample_elem }
    print(hemispheres)
    return hemispheres