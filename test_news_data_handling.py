"""Module that test the news data handling module functions"""
import json
import requests
import logging
import sched
import time
from covid_news_handling import news_API_request
from covid_news_handling import update_news

style = '%(levelname)s: %(asctime)s %(message)s'
logging.basicConfig(filename='sys.log', format=style)
s = sched.scheduler(time.time, time.sleep)


def test_news_API_request():
    """Test that the news api request has defult covid terms set as an argument"""
    assert news_API_request()
    assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()
def test_response_news():
    """Testing the request-response cycle of the news API"""
    with open('config.json', 'r') as config_json:
        config = json.load(config_json)
        api_key = config["API_keys"]["news"]
    # Choosing to access UK news articles
    base_url = "https://newsapi.org/v2/top-headlines?"
    api_key = config['API_keys']['news']
    country = "gb"
    complete_url = base_url + "country=" + country + "&apiKey=" + api_key
    response = requests.get(complete_url)
    # Confirm that the request-response cycle completed successfully.
    assert response.status_code <= 400
def test_update_news():
    """Test that you can update the news"""
    update_news(10,'test')

while __name__ == '__main__':
    # Schdule all the test to run every hour
    try:
        s.enter(3600, 1, test_news_API_request)
        s.enter(3600, 1, test_response_news)
        s.enter(3600, 1, test_update_news)
        s.run(blocking=False)
    # If a test fails it should be logged as an error
    except AssertionError as warnign:
        logging.error("FAILED TEST")