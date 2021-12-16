"""Module that uses the News API to ctreate a list of news with the relevant Key Terms"""
import time
import sched
import json
import logging
import requests
from time_manipulation import hhmm_to_seconds, current_time
from covid_data_handler import update



s = sched.scheduler(time.time, time.sleep)
logging.basicConfig(filename='sys.log')
# Open configuration file to get data from it
with open('config.json', 'r') as config_json:
    config = json.load(config_json)


def news_API_request(covid_terms = 'Covid COVID-19 coronavirus') -> list:
    """Function that takes an argument of Covid Terms are used to return a list of dictionaries
    of article title and article content from news with the Covid Terms in them"""
    base_url = "https://newsapi.org/v2/top-headlines?"
    api_key = config['API_keys']['news']
    country = "gb"
    complete_url = base_url + "country=" + country + "&apiKey=" + api_key
    response = requests.get(complete_url)
    # Log if the API request returns an error
    if response.status_code >= 400:
        logging.warning("Failed to pull news")
    news = response.json()
    articles = news['articles']
    filt = ''.join(covid_terms).split()
    news_list = []
    seen = []
    # Filter through the news articles with the covid terms
    for term in filt:
        for article in articles:
            if term.lower() in str(article).lower():
                news_list.append({
                    'title': article['title'],
                    'content': article['content']
                })
    # Remove any duplicate stories
    for stories in news_list:
        if stories not in seen:
            seen.append(stories)
    # Write the articles onto a json file
    with open('news.json', 'w') as news_jason:
        json.dump(seen, news_jason)
    return seen
def update_news(update_interval: float, update_name: str) -> json:
    """Function that updates the COVID data for a certain time interval and returns
    the name of the Update"""
    update.append(
        {'title':update_name,
        'content':'There has been a Covid Data update scheduled',
        'time': hhmm_to_seconds(current_time()) + int(update_interval)}
    )
    with open('update.json', 'w') as update_jason:
        json.dump(update, update_jason)
    s.enter(update_interval, 1, news_API_request)
    return update_jason

if __name__ == '__main__':
    update_news(2, 'test')
    s.run()
             