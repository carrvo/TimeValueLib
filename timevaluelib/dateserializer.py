"""
Date manipulation functions.
"""

import datetime

import timevaluelib

def parseDate(date, format=None):
    """
    Parses a date from a string or copies a datetime.date object.

    @Params:
        - date: to be parsed
        - format: the string format the date parameter is represented as
    """
    if isinstance(date, datetime.date):
        return datetime.date(date.year, date.month, date.day)
    elif format:
        return datetime.datetime.strptime(date, format).date()
    elif timevaluelib.DATE_FORMAT:
        return datetime.datetime.strptime(date, timevaluelib.DATE_FORMAT).date()
    else:
        return datetime.date.fromisoformat(date)

def formatDate(date, format=None):
    """
    Formats a date into a string.

    @Params:
        - date: to be formatted
        - format: the string format the date parameter will be represented as
    """
    if format:
        return date.strftime(format)
    elif timevaluelib.DATE_FORMAT:
        return date.strftime(timevaluelib.DATE_FORMAT)
    else:
        return date.isoformat()
