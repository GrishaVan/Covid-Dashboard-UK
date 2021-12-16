"""Module that processes covid data from a csv file"""
import csv
import sched
import logging
import time
import json
from time_manipulation import hhmm_to_seconds, current_time
from uk_covid19 import Cov19API

s = sched.scheduler(time.time, time.sleep)
logging.basicConfig(filename='sys.log')
update = []

def parse_csv_data(csv_filename: any) -> csv:
    """Function to open, read and return the values of a csv file in a list"""
    lines = open(csv_filename, 'r').readlines()
    return lines
def process_covid_csv_data(covid_csv_data: csv) -> int:
    """Function that processes a covid csv file and finds total deaths,
    current hospital cases, and last 7 day cases"""
    reader = csv.reader(covid_csv_data, delimiter=',')
    header = next(reader)
    # Delete the headers of the csv file
    del header
    data = list(reader)
    cummilative = []
    hospital = []
    new_cases = []
    # Split the data into different categories
    for row in data:
        cummilative.append(row[4])
        hospital.append(row[5])
        new_cases.append(row[6])
    total_deaths = 0
    last7days_cases = 0
    i = 0
    # Removing any empty data points from the list and then finding the finding
    # the last 7 day infection rate, current hospital cases, and total deaths
    for days in new_cases[0:9]:
        if len(days) == 0:
            new_cases.remove(days)
    for days in new_cases[1:8]:
        last7days_cases += int(days)
    for days in hospital:
        if len(days) == 0:
            i += 1
        else:
            current_hospital_cases = int(hospital[i])
            break
    for days in cummilative:
        if len(days) == 0:
            i += 1
        else:
            total_deaths = int(cummilative[i])
            break
    return last7days_cases, current_hospital_cases, total_deaths
def covid_API_request(location ='Exeter', location_type ='ltla') -> dict:
    """Function to get the covid cases by day in a UK city from the API"""
    city = [
        'areaType=' + location_type,
        'areaName=' + location
    ]
    cases = {
        'date': 'date',
        'city': 'areaName',
        'cases': 'newCasesByPublishDate'
    }
    local_api = Cov19API(filters=city, structure=cases)
    local = local_api.get_json()
    return local
def local_infection(file: dict) -> int:
    """Function that takes a dictionary of the local covid cases
    and return the 7 day infection rate"""
    data = file['data']
    total_cases = []
    # From the Covid API add the cases by day into a list
    for items in data:
        total_cases.append(items['cases'])
    local_week_total = 0
    i = 0
    # Loop that sums up the last 7 day cases
    for day in total_cases:
        while i <= 6:
            if day is None:
                total_cases.remove(day)
            else:
                local_week_total += total_cases[i]
                i += 1
    return local_week_total
def national_local_api_request(location_type ='overview') -> dict:
    """Function that take values from the Covid19 API request processes them and
    return a dictionary with the national 7 day infection rate, total deaths,
    and current hospital cases"""
    england = [
        'areaType=' + location_type
    ]
    cases_death_hospital = {
        'date': 'date',
        'country': 'areaName',
        'cases': 'newCasesByPublishDate',
        'deaths': 'cumDeaths28DaysByDeathDate',
        'hospital': 'hospitalCases'
    }
    national_api = Cov19API(filters=england, structure=cases_death_hospital)
    nation = national_api.get_json()
    data = nation['data']
    total_cases = []
    total_deaths = []
    total_hospital = []
    national_week_total = 0
    i = 0
    # From the API split the data into cases by day, hospital xases, and total deaths
    for items in data:
        total_cases.append(items['cases'])
        total_deaths.append(items['deaths'])
        total_hospital.append(items['hospital'])
    # Removing any empty data points and getting national infection, hospital cases, and
    # Total deaths
    for day in total_cases:
        while i <= 6:
            if day is None:
                total_cases.remove(day)
            else:
                national_week_total += total_cases[i]
                i += 1
    for day in total_deaths:
        if day is None:
            total_deaths.remove(day)
    deaths = total_deaths[0]
    for day in total_hospital:
        if day is None:
            total_hospital.remove(day)
    hospital_cases = total_hospital[0]
    # Return a dictionary of the values
    national_info = {
        'infection': national_week_total,
        'deaths': deaths,
        'hospital': hospital_cases,
        'localInfection': local_infection(covid_API_request())
    }
    # Write all the data onto a json file
    with open('data.json', 'w') as data_jason:
        json.dump(national_info, data_jason)
    return national_info
def schedule_covid_updates(update_interval: float, update_name: str) -> json:
    """Function that updates the COVID data for a certain time interval and returns
    the name of the Update"""
    s.enter(update_interval, 1, national_local_api_request)
    update.append(
        {'title':update_name,
        'content':'There has been a Covid update scheduled',
        'time': hhmm_to_seconds(current_time()) + int(update_interval)}
    )
    with open('update.json', 'w') as update_jason:
        json.dump(update, update_jason)
    return update_jason


if __name__ == '__main__':
    schedule_covid_updates(2, 'test')
