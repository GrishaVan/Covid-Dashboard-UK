"Module that uses flask as a html backend to display the Covid Dashboard"
import json
import logging
import time
import sched
from covid_data_handler import national_local_api_request, schedule_covid_updates
from covid_data_handler import update
from flask import Flask
from flask import render_template
from flask import request
from covid_news_handling import news_API_request, update_news
from time_manipulation import hhmm_to_seconds, current_time, difference_in_time

app = Flask(__name__)
style = '%(levelname)s: %(asctime)s %(message)s'
logging.basicConfig(filename='sys.log', format=style)
# Only logs beyond WARNING severity level
logging.getLogger("werkzeug").setLevel('WARNING')


s = sched.scheduler(time.time, time.sleep)
removed = []
updates = update

@app.route('/index')
def covid_data():
    """Function to get the html page up and running, to show all the news
    Covid data, and the current news"""
    s.run(blocking=False)
    # Assigning the queryes to variables
    logging.info('All good')
    name = request.args.get('two')
    timing = request.args.get('update')
    update_data = request.args.get('covid-data')
    add_news = request.args.get('news')
    repeat = request.args.get('repeat')
    stories, national_info = get_data()
    news: bool = False
    data: bool = False
    repeat: bool = False
    # Checks if an update has been schduled
    if name:
        if add_news:
            news: bool = True
        if update_data:
            data: bool = True
        if repeat:
            repeat: bool = True
        # If the time for the update has passed log it and do nothing
        if hhmm_to_seconds(timing) <= hhmm_to_seconds(current_time()) and not repeat:
            logging.warning('Update set for a time that passed')
        else:
            # Checks what type of update to schedule
            schedule_updates(news, data, timing, name, repeat)
    else:
        # If nothing is inpited covid data will refresh every 6 hours while the news every hour
        # To make sure the user dosent miss out on any new occuring events
        refresh_data(6*3600, name)
        refresh_news(3600, name)
    remove_news = request.args.get('notif')
    # If article has been removed add it to the removed list
    for articles in stories:
        # Checks if "x" has been clicked on a news article, if so add it to the removed list
        if remove_news == articles['title']:
            stories.remove(articles)
            removed.append(articles)
    # Update the removed and news json files
    with open('removed.json', 'w') as removed_json:
        json.dump(removed, removed_json)
    with open('news.json', 'w') as news_json:
        json.dump(stories, news_json)
    remove_update()
    delete_update = request.args.get('update_item')
    # Checks the every update set. Refreshes the needed data and if update is not on repeat,
    # remove it from the list
    for items in update:
        index = update.index(items)
        # Checks if the "x" has been clicked on the update to remove it
        if items['title'] == delete_update:
            update.remove(items)
            s.cancel(s.queue[index])
    return render_template('index.html',
        title='Covid Tracker',
        location='Exeter',
        local_7day_infections=national_info['localInfection'],
        nation_location='United Kingdom',
        national_7day_infections= national_info['infection'],
        hospital_cases='Hospital cases: ' + str(national_info['hospital']),
        deaths_total='Total Deaths: ' + str(national_info['deaths']),
        favicon= 'http://pm1.narvii.com/6501/87684f32028371314aec14f160e72ef64ab6d74c_00.jpg',
        news_articles= stories[0:4],
        updates= updates)



def get_data() -> list:
    """Opens json files containing the news articles and the Covid-19 Data"""
    with open('news.json', 'r') as news_json:
        stories = json.load(news_json)
    # If story is in the removed json it will not reapear when the news are updated
    with open('removed.json', 'r') as removed_json:
        filtered_news = json.load(removed_json)
        for news in stories:
            if stories in filtered_news:
                news.remove(stories)
    with open('data.json', 'r') as data_json:
        national_info = json.load(data_json)
    return stories, national_info
def schedule_updates(news: bool, data: bool, interval: str, title: str, repeat: bool) -> list:
    """Function to schedule an update depending in what bool (boxes)
    where checked in the html page"""
    # Changes the inputed string of time into a int value of difference between
    # the current time and the inoputed time in seconds
    timing = difference_in_time(interval)
    # If not repeated news set a single update depending on which bool is True
    if not repeat:
        if news and not data:
            refresh_news(timing, title)
        if data and not news:
            refresh_data(timing, title)
        if data and news:
            refresh_news(timing, title)
            refresh_data(timing, title)
    # If repeated news than set an update accoriding to the true bool, and then,
    # update on a daily basis
    else:
        if news and not data:
            refresh_news(timing, title)
            periodic(1, refresh_news, (24*3600, title))
        if data and not news:
            refresh_data(timing, title)
            periodic(1, refresh_data, (24*3600, title))
        if data and news:
            refresh_news(timing, title)
            refresh_data(timing, title)
            periodic(1, refresh_news, (24*3600, title))
            periodic(1, refresh_data, (24*3600, title))
def remove_update() -> list:
    """Function that as soon as an update completes it is removed from the
    list of currentley ongoing updates"""
    for items in update:
        # If the value of the update item time is samlelr than the actual time
        # (when updaet is completed) the update will be removed from the list
        if items['time'] <= hhmm_to_seconds(current_time()):
            update.remove(items)
def refresh_news(timing: int, name: str) -> list:
    """Function that refreshes the news and adds an item to the currentley
    ongoing updates list"""
    # If an update is set, then create an update item and add it to the list of updates
    if name:
        update_news(timing, name)
        s.enter(timing, 1, news_API_request)
    # If an update is not set, then just refresh the data
    else:
        s.enter(timing, 1, news_API_request)
def refresh_data(timing: int, name: str) -> list:
    """Function that refreshes the Covid Data and adds an item to the currentley
    ongoing updates list"""
    # If an update is set, then create an update item and add it to the list of updates
    if name:
        schedule_covid_updates(timing, name)
        s.enter(timing, 1, national_local_api_request)
    else:
    # If an update is not set, then just refresh the data
        s.enter(timing, 1, national_local_api_request)
def periodic(interval: int, action, actionargs=()) -> None:
    """Fucntion that periodicaly calls anoter function"""
    # Keep calling a function on a periodic basis being the interval
    s.enter(interval, 1, periodic, (interval, action, actionargs))
    action(*actionargs)
    s.run()

if __name__ == '__main__':
    # If the news and covid data json files are empty, this will instantly update them
    national_local_api_request()
    news_API_request()
    app.run()
    