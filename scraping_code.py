import requests
from bs4 import BeautifulSoup
import numpy as np
# import matplotlib.pyplot as plt
import tkinter
import json
from textblob import TextBlob
import sys   
import re  

# stock price and stock trend
def stock_info(name):
    stock_data = {}
    url_smy = 'https://www.nasdaq.com/symbol/' + str(name)
    web_data_smy = requests.get(url_smy)
    soup_smy = BeautifulSoup(web_data_smy.text, 'lxml')
    urls_smy_price = soup_smy.select('div #qwidget_lastsale')
    stock_price = str(urls_smy_price).replace('>','<').split('<')[2]

    urls_smy_trend = soup_smy.select('div #qwidget-arrow')
    trend_color = str(urls_smy_trend).replace('"','-').split('-')[5]
    
#     stock_data = {'company': name, 'price' : stock_price, 'trend' : trend_color}


# stock history: date and open price
# oxy stock history
def stock_history(name):
    url_stkhis = 'https://www.nasdaq.com/symbol/' + str(name) + '/historical'
    web_data_stkhis = requests.get(url_stkhis)
    soup_stkhis = BeautifulSoup(web_data_stkhis.text, 'lxml')
    stkhis_price = str(soup_stkhis.select('div #quotes_content_left_pnlAJAX td')).split()
    temp = []
    for i in range(len(stkhis_price)):
        if (i % 3 == 1):
            temp.append(stkhis_price[i])
    date = []
    open_price = []
    for j in range(len(temp)):
        if (j % 6 == 0):
            date.append(temp[j])
        if (j % 6 == 1):
            open_price.append(temp[j])
    return (date,open_price)

# oxy news: news title and news links
# oxy news
def news_info(name):
    news_data = {}
    url_news = 'https://www.nasdaq.com/symbol/' + str(name) + '/news-headlines'
    web_data_news = requests.get(url_news)
    soup_news = BeautifulSoup(web_data_news.text, 'lxml')
    urls_all_news = soup_news.select('span.fontS14px > a') 
    # get all information about news including titles and urls

    url_news_host = 'https://www.nasdaq.com/article/'
    news_url = [] # store all news url in here
    for link in urls_all_news:
        if link.text.isspace():
            continue
        else:
            page_url = url_news_host + link.get('href')
            news_url.append(page_url)

    news_list = str(urls_all_news).replace('">','</a>').split('</a>')
    num = len(news_list)
    news_title = [] # store all news title in here
    for n in range(num):
        if (n % 2 == 1):
            news_title.append(news_list[n])
    
    polarity = []
    for link in news_url:
        web_data_url = requests.get(link)
        soup_url = BeautifulSoup(web_data_url.text, 'lxml')
        # soup_url
        article = str(soup_url.select('div #articleText'))
        article = re.sub('<.*?>', "", article)
        blob = TextBlob(article)
        polarity.append(blob.sentiment.polarity)

    return news_url,news_title, polarity
    
# oxy marketcap
def marketcap_info(name):
    url_smy = 'https://www.nasdaq.com/symbol/' + name
    web_data_smy = requests.get(url_smy)
    soup_smy = BeautifulSoup(web_data_smy.text, 'lxml')
    urls_smy_price = soup_smy.select('div.table-cell')
    str_temp = str(urls_smy_price).replace('</b>','<b>').split('<b>')
    loc_mc = str_temp.index('Market Cap')
    market_cap = str_temp[loc_mc + 1].split('\r\n')[1].replace(" ","")
    return market_cap

# oxy cash flow
def cashflow_info(name):
    url_smy = 'https://www.nasdaq.com/symbol/' + name + '/financials?query=income-statement'
    web_data_smy = requests.get(url_smy)
    soup_smy = BeautifulSoup(web_data_smy.text, 'lxml')
    if len(soup_smy.select('tr.net > td')) > 0:
        cash_flow = list(soup_smy.select('tr.net > td')[1])
    else:
        cash_flow = ['None']
    return cash_flow

def sentiment(name):
    news_url, news_list = news_info(name)
    polarity = []
    for link in news_url:
        web_data_url = requests.get(link)
        soup_url = BeautifulSoup(web_data_url.text, 'lxml')
        # soup_url
        article = str(soup_url.select('div #articleText'))
        article = re.sub('<.*?>', "", article)
        blob = TextBlob(article)
        polarity.append(blob.sentiment.polarity)
    return polarity