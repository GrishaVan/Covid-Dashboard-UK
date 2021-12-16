"""Module that takes care of time conversion from string to integer,
can get the current time, and will tell a diference between, inputed
and current time in seconds"""
import logging
import time

def minutes_to_seconds( minutes: str ) -> int:
    """Converts minutes to seconds"""
    return int(minutes)*60
def hours_to_minutes( hours: str ) -> int:
    """Converts hours to minutes"""
    return int(hours)*60
def hhmm_to_seconds( hhmm: str ) -> int:
    """Converts time in form HH:MM into seconds"""
    # Checks if time inputed in the right format
    if len(hhmm.split(':')) != 2:
        logging.error('Wrong time format')
    return minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + \
        minutes_to_seconds(hhmm.split(':')[1])
def current_time() -> str:
    """Function to get current time"""
    current_time = str(time.gmtime().tm_hour) + ":" + str(time.gmtime().tm_min)
    return current_time
def difference_in_time(interval:str) -> int:
    """Finds the differnce from the selted time to the current time in seconds"""
    return hhmm_to_seconds(interval) - hhmm_to_seconds(current_time())

if __name__ == '__main__':
    current_time()
