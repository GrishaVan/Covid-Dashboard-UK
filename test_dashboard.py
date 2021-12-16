"""Module that test the dashbord module functions"""
from dashboard import get_data, periodic, refresh_data, refresh_news, schedule_updates
import logging
import sched
import time

s = sched.scheduler(time.time, time.sleep)
style = '%(levelname)s: %(asctime)s %(message)s'
logging.basicConfig(filename='sys.log', format=style)

def test_get_data():
    """Test that the get data function returns the news in a list and the covid data,
    in a dictionary"""
    news, data = get_data()
    assert isinstance(news, list)
    assert isinstance(data, dict)
def test_schedule_updates():
    """Test that a scheduled update can be set"""
    news: bool = True
    data: bool = False
    repeat: bool = False
    schedule_updates(news, data, "12:00", 'Hello', repeat)
def test_refresh_news():
    """Test that the news can be updated"""
    refresh_news(2, 'test')
def test_refresh_data():
    """Test that the covid data can be updated"""
    refresh_data(2, 'test')

while __name__ == '__main__':
    # Schdule all the test to run every hour
    try:
        s.enter(3600, 1, test_get_data)
        s.enter(3600, 1, test_schedule_updates)
        s.enter(3600, 1, test_refresh_news)
        s.enter(3600, 1, test_refresh_data)
        s.run(blocking=False)
    # If a test fails it should be logged as an error
    except AssertionError as warnign:
        logging.error("FAILED TEST")
