"""Module to test that the time manipulation module functions"""
from time_manipulation import current_time, difference_in_time, hhmm_to_seconds, hours_to_minutes, minutes_to_seconds
import logging
import sched
import time

s = sched.scheduler(time.time, time.sleep)
style = '%(levelname)s: %(asctime)s %(message)s'
logging.basicConfig(filename='sys.log', format=style)

def test_minutes_to_seconds():
    """Test that the the conversion is correct and test that the seconds are
    integers"""
    minute = minutes_to_seconds('1')
    assert isinstance(minute, int)
    assert 60 == minute
def test_hours_to_minutes():
    """Tetst that the conversion from hours to minutes is correct,
    and that the hours are integers"""
    hour = hours_to_minutes('2')
    assert isinstance(hour, int)
    assert 120 == hour
def test_hhmm_to_seconds():
    """Tetst to see if the conversion in the form HH:MM to seconds works properly"""
    mid_day = hhmm_to_seconds('12:00')
    assert isinstance(mid_day, int)
    assert 12*3600 == mid_day
def test_current_time():
    """Test that the current time is a string in from of HH:MM and that it is
    converted into seconds"""
    time = current_time()
    assert isinstance(time, str)
    seconds = hhmm_to_seconds(current_time())
    assert isinstance(seconds, int)
def test_difference_in_time():
    """Test that the differnce in time to our cutrrent time in an integre, and that
    the difference between now and the current time is 0"""
    now = difference_in_time(current_time())
    assert isinstance(now, int)
    assert now == 0

while __name__ == '__main__':
    # Schdule all the test to run every hour
    try:
        s.enter(3600, 1, test_minutes_to_seconds)
        s.enter(3600, 1, test_hours_to_minutes)
        s.enter(3600, 1, test_hhmm_to_seconds)
        s.enter(3600, 1, test_current_time)
        s.enter(3600, 1, test_difference_in_time)
        s.run(blocking=False)
        #  If a test fails it should be logged as an error
    except AssertionError as warnign:
        logging.error("FAILED TEST")
