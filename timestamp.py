"""
timestamp.py

Contains methods for timestamp functionality.

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

TODO: Look for a way to make raising errors not so repetitive. Maybe add another function to do so?

"""

# Import the datetime module as dt
import datetime as dt

# Import the ast module for the ast.literal_eval method 
import ast

def active_at_time(timestamp: str, properties: str) -> bool:
    """
    Returns whether at the specific date and time, the element with properties <properties> was active.

    :param timestamp: A string of format "YYYY-MM-DD HH:MM:SS.XXXXXX", equivalent to the Python datetime.datetime object of format "%Y-%m-%d %H:%M:%S".
    :type timestamp: str
    :param properties: A string of Python syntax containing a Python list containing dictionaries at each index that containg keys "datetime" (of which the corresponding value is a string of datetime.datetime format "%Y-%m-%d %H:%M:%S") and "active" (of which the corresponding value is a boolean, either True or False). The list MUST be sorted such that the times appear in order.
    :type properties: str
    :return: Returns whether at the specific timestamp represented by <datetime>, the element with properties <properties> is active.
    :rtype: bool
    """

    format = "%Y-%m-%d %H:%M:%S"

    # convert the time into a datetime.datetime object
    time = dt.datetime.strptime(timestamp, format)

    # Convert properties into an actual Python object
    props = ast.literal_eval(properties)

    # props should be a list.
    if not isinstance(props, list):
        raise TypeError('properties must be a string containing a Python list of dictionaries.')

    # If the list is empty, return False.
    if len(props) == 0:
        return False

    # Check edge case where if time < first time, instantly return False.
    if isinstance(props[0], dict):
        if "timestamp" in props[0]:
            time_0 = dt.datetime.strptime(props[0]["timestamp"], format)
            if time < time_0:
                return False
        else:
            raise ValueError(f"properties does not have a 'timestamp' key at index 0")
    else:
        raise TypeError('properties must be a string containing a Python list of dictionaries.')


    # Perform binary search on the props
    l, r, mid = 0, len(props) - 1, 0

    while l <= r:

        mid = l + (r - l) // 2

        # Ensure that props[mid] is a dict.
        if not isinstance(props[mid], dict):
            raise TypeError('properties must be a string containing a Python list of dictionaries.')

        # Ensure that "timestamp" is a property of props[mid]
        if "timestamp" in props[mid]:

            time_mid = dt.datetime.strptime(props[mid]["timestamp"], format)

            # If the queried time is later than the time being looked at
            if time > time_mid:
                l = mid + 1
            
            # If the queried time is less than the time being looked at
            elif time < time_mid:
                r = mid - 1

            # If the queried time is EXACTLY the time being looked at.
            else:
                if "active" in props[mid]:
                    return props[mid]["active"]
                else:
                    raise ValueError(f"properties does not have an 'active' key at index {mid}")

        else:
            raise ValueError(f"properties does not have a 'timestamp' key at index {mid}")

    if l <= 0:
        return False

    # If the binary search has completed, the time specified by <time> is between props[l] and props[r].
    if "active" in props[l - 1]:
        return props[l - 1]["active"]
    else:
        raise ValueError(f"properties does not have an 'active' key at index {l - 1}")
