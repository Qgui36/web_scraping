from bs4 import BeautifulSoup
import requests
import pandas as pd


def scrape_info():
    url = 'https://mars.nasa.gov/news/'
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')
    # find the latest news 
    result = soup.find('div',class_="slide")
    title=result.find('div',class_="content_title").text.strip()
    description=result.find('div',class_="rollover_description").text.strip()

    url_img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    response = requests.get(url_img)
    soup = BeautifulSoup(response.text, 'html.parser')
    results_img = soup.find_all('a',class_="fancybox")
    img=results_img[5]
    link=img["data-fancybox-href"]
    featured_image_url=f"https://www.jpl.nasa.gov{link}"

    url_weather = 'https://twitter.com/marswxreport?lang=en'
    # Retrieve page with the requests module
    response = requests.get(url_weather)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')
    # return latest weather result
    result = soup.find('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    mars_weather=result.text
    mars_weather=mars_weather.replace('\n', ', ')

    url_facts = 'https://space-facts.com/mars/'
    table = pd.read_html(url_facts)
    mars_facts=table[0]
    mars_facts.rename(columns={0:"description",1:"value"},inplace=True)
    mars_facts.set_index('description', inplace=True)
    html_table = mars_facts.to_html()
    
    url_img = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url_img)
    soup = BeautifulSoup(response.text, 'lxml')
    inf = soup.find_all('div',class_="item")
    hemisphere_image_urls=[]
    dict={}
    key1="title"
    key2="img_url"
    for i in inf:
        hem_title=i.find('h3').text.replace(' Enhanced', '')
        dict[key1]=hem_title
        link=i.find('a', class_="itemLink product-item")
        link_change=link['href'].replace('/search/map/','https://astropedia.astrogeology.usgs.gov/download/')
        final_link=f"{link_change}.tif/full.jpg"
        dict[key2]=final_link
        hemisphere_image_urls.append(dict.copy())   

    mars_data={}
    mars_data["latest_news_title"]=title
    mars_data['latest_news_description']=description
    mars_data['featured_image_url']=featured_image_url
    mars_data['mars_weather']=mars_weather
    mars_data['mars_facts']=html_table
    mars_data['hemisphere_images']=hemisphere_image_urls

    # Return results
    return mars_data

