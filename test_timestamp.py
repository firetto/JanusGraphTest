"""
test_timestamp.py

Contains methods for testing timestamp functionality.

FOR NOW, vertices and edge properties will have the following structure:
    Each vertex/edge has a property called "properties" which is a list (array) of dictionaries (maps):
    [
        {
            "timestamp": "<YYYY-MM-DD HH:MM:SS>",           # Note that SS can be a float, as long as the decimal of SS is at most 6 digits: SS.XXXXXX. 
                                                            # This is the string representation of a datetime.datetime object of format "%Y-%m-%d %H:%M:%S"

            "active": <bool>,                               # Could be True or False.
            ...                                             # Could have other properties as well
        },
        {
            ...                                              # Of same format as above.
        },
        ...
    ]
"""

# import active_at_time
from timestamp import active_at_time

# Import the datetime module as dt
import datetime as dt

# Import pytest to test the function
import pytest


def test_active_at_time_empty():
    """
    Test active_at_time with an empty list.
    """

    time = dt.datetime(2002, 8, 10)

    props = []

    assert active_at_time(str(time), str(props)) == False


def test_active_at_time_bad_list_syntax():
    """
    Test active_at_time with a property string that is not in valid Python syntax.
    """

    time = dt.datetime(2002, 8, 10)

    bad_string = "dfiuhgydfguiohdfgiuohdfguihodfguhidfg"

    with pytest.raises(ValueError):
        active_at_time(str(time), bad_string)

def test_active_at_time_not_list():
    """
    Test active_at_time with a property string that is not in valid Python syntax.
    """

    time = dt.datetime(2002, 8, 10)

    bad_string = "{'hello'}"

    with pytest.raises(TypeError):
        active_at_time(str(time), bad_string)


def test_active_at_time_bad_time():
    """
    Test active_at_time with a time string that is not in "%Y-%m-%d %H:%M:%S" datetime.datetime format.
    """

    bad_time = "today"

    props = [
        {
            "timestamp": str(dt.datetime(2002, 8, 10)),
            "active": True
        }
    ]

    with pytest.raises(ValueError):
        active_at_time(bad_time, str(props))


def test_active_at_time_has_time_1():
    """
    Test active_at_time with a time that is in a dictionary in the properties.
    """

    time = dt.datetime(2002, 8, 10)

    props = [
        {
            "timestamp": str(dt.datetime(1997, 6, 6)),
            "active": False
        },
        {
            "timestamp": str(dt.datetime(2002, 8, 10)),
            "active": True
        },
        {
            "timestamp": str(dt.datetime(2011, 7, 20)),
            "active": False
        },
    ]

    assert active_at_time(str(time), str(props)) == True

def test_active_at_time_has_time_2():
    """
    Test active_at_time with a time that is in a dictionary in the properties.
    """

    time = dt.datetime(2002, 8, 10, 2, 48, 48)

    props = [
        {
            "timestamp": str(dt.datetime(1997, 6, 6, 23, 19, 48)),
            "active": True
        },
        {
            "timestamp": str(time),
            "active": False
        },
        {
            "timestamp": str(dt.datetime(2011, 7, 20, 20, 11, 10)),
            "active": True
        },
    ]

    assert active_at_time(str(time), str(props)) == False


def test_active_at_time_inbetween_1():
    """
    Test active_at_time with a time that is inbetween two entries in dictionary.
    """

    time = dt.datetime(2002, 8, 10, 2, 48, 48)

    props = [
        {
            "timestamp": str(dt.datetime(1997, 6, 6, 23, 19, 48)),
            "active": False
        },
        {
            "timestamp": str(dt.datetime(2002, 8, 10, 2, 48, 47)),
            "active": True
        },
        {
            "timestamp": str(dt.datetime(2002, 8, 10, 2, 48, 49)),
            "active": False
        },
        {
            "timestamp": str(dt.datetime(2011, 7, 20, 20, 11, 10)),
            "active": False
        },
    ]

    assert active_at_time(str(time), str(props)) == True


def test_active_at_time_inbetween_2():
    """
    Test active_at_time with a time that is inbetween two entries in dictionary.
    """

    time = dt.datetime(2002, 8, 10)

    props = [
        {
            "timestamp": str(dt.datetime(1997, 6, 6, 23, 19, 48)),
            "active": False
        },
        {
            "timestamp": str(dt.datetime(2001, 8, 10)),
            "active": False
        },
        {
            "timestamp": str(dt.datetime(2003, 8, 10)),
            "active": False
        },
        {
            "timestamp": str(dt.datetime(2011, 7, 20, 20, 11, 10)),
            "active": True
        },
    ]

    assert active_at_time(str(time), str(props)) == False

def test_active_at_time_inbetween_3():
    """
    Test active_at_time with a time that is inbetween two entries in dictionary.
    """

    time = dt.datetime(2002, 8, 10)

    props = [
        {
            "timestamp": str(dt.datetime(2001, 8, 10)),
            "active": True
        },
        {
            "timestamp": str(dt.datetime(2003, 8, 10)),
            "active": False
        },
        {
            "timestamp": str(dt.datetime(2011, 7, 20, 20, 11, 10)),
            "active": True
        },
    ]

    assert active_at_time(str(time), str(props)) == True



def test_active_at_time_before_first_1():
    """
    Test active_at_time with a time that is before the first time in the list. 
    """

    time = dt.datetime(2002, 8, 10)

    props = [
        {
            "timestamp": str(dt.datetime(2011, 7, 20, 20, 11, 10)),
            "active": False
        },
        {
            "timestamp": str(dt.datetime(2012, 7, 20)),
            "active": True
        },
    ]

    assert active_at_time(str(time), str(props)) == False

def test_active_at_time_before_first_2():
    """
    Test active_at_time with a time that is before the first time in the list. 
    """

    time = dt.datetime(2002, 8, 10)

    props = [
        {
            "timestamp": str(dt.datetime(2011, 7, 20, 20, 11, 10)),
            "active": True
        },
        {
            "timestamp": str(dt.datetime(2011, 8, 20, 20, 11, 10)),
            "active": True
        },
        {
            "timestamp": str(dt.datetime(2011, 9, 20, 20, 11, 10)),
            "active": True
        },
        {
            "timestamp": str(dt.datetime(2012, 7, 20)),
            "active": True
        },
    ]

    assert active_at_time(str(time), str(props)) == False


