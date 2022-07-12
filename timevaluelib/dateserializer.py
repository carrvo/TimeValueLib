
import datetime

import timevaluelib

def parseDate(date, format=None):
    if isinstance(date, datetime.date):
        return datetime.date(date.year, date.month, date.day)
    elif format:
        return datetime.datetime.strptime(date, format).date()
    elif timevaluelib.DATE_FORMAT:
        return datetime.datetime.strptime(date, timevaluelib.DATE_FORMAT).date()
    else:
        return datetime.date.fromisoformat(date)

def formatDate(date, format=None):
    if format:
        return date.strftime(format)
    elif timevaluelib.DATE_FORMAT:
        return date.strftime(timevaluelib.DATE_FORMAT)
    else:
        return date.isoformat()
