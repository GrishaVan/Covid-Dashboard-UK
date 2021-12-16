"""Module to test the covid data handler module functions"""
import sched
import time
import logging
from covid_data_handler import local_infection, national_local_api_request, parse_csv_data
from covid_data_handler import process_covid_csv_data
from covid_data_handler import covid_API_request
from covid_data_handler import schedule_covid_updates

style = '%(levelname)s: %(asctime)s %(message)s'
logging.basicConfig(filename='sys.log', format=style)
s = sched.scheduler(time.time, time.sleep)

def test_parse_csv_data():
    """Test the lenght parse csv data function"""
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639
def test_process_covid_csv_data():
    """Test the process covid csv data that the values where,
    correctly calculated"""
    last7days_cases , current_hospital_cases , total_deaths = \
        process_covid_csv_data(parse_csv_data('nation_2021-10-28.csv'))
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544
def test_covid_API_request():
    """Test Covid Api request function returns a dictionary of values"""
    data = covid_API_request()
    second = covid_API_request(location='Exeter', location_type='ltla')
    assert isinstance(data, dict)
    assert data == second
def test_local_infection():
    """Test local infection function to make sure the value is an integer"""
    infection = local_infection(covid_API_request())
    assert isinstance(infection, int)
def test_national_local_api_request():
    """Test that national local api request has a defult value for the argument"""
    data = national_local_api_request()
    second = national_local_api_request(location_type='overview')
    assert data == second
    assert isinstance(data, dict)
def test_schedule_covid_updates():
    """Test that a schedule covid update can be done"""
    schedule_covid_updates(update_interval=10, update_name='update test')

while __name__ == '__main__':
    # Schdule all the test to run every hour
    try:
        s.enter(3600, 1, test_parse_csv_data)
        s.enter(3600, 1, test_process_covid_csv_data)
        s.enter(3600, 1, test_covid_API_request)
        s.enter(3600, 1, test_local_infection)
        s.enter(3600, 1, test_national_local_api_request)
        s.enter(3600, 1, test_schedule_covid_updates)
        s.run(blocking=False)
    # If a test fails it should be logged as an error
    except AssertionError as warnign:
        logging.error("FAILED TEST")
