"""
@THEORY:
The time-value property of money comes from the existence and calcuation of interest.

Basic Theory defines four variables:
    - Principle Amount (P): the amount you have today
        (may also be called "Present Amount")
    - Amount of Interest (I): compensation paid to a lender
    - Interest Rate (i): usually expressed as a percentage of P
    - Future Amount (F): the value of your P at a future date
This gives rise to the equation: F = P + I where I = P * i
    which can be re-written (in the common form) as F = P * (1 + i)
As such, the value of money is tied intrinsically to the concept of time.
Meaning that two amounts of money from different times cannot interact
until a conversion has been made.

This is immediately enhanced with the concept of
compound interest over a number of periods.
By doing so the equation is modified to become:
    F = P * (1 + i)**N where N is the number of periods

"""

import datetime
Date = lambda date, format: datetime.datetime.strptime(date, format).date() if not isinstance(date, datetime.date) else Date(date.strftime(format), format)

#from TimeValueLib.Interest import Interest

class TimeValue(object):
    """
    Class for representing the time-value property of money (monetary).

    Specifically objects of this class will always hold the relative P.
        This is "relative P" instead of just "P" because it recognizes
        that you can make many time conversions of money and so what
        consitutes "P" changes relative to the time it corresponds to.
        Thus this class treats the "value" as being the P relative to
        the object's concept of time. The object's concept of time is
        that of the Economical time and not the object's life.

    Furthermore, this class recognizes that the conversion backward in time
        (where you would treat the "current" as being the "F" and the past
        as being the "P") is the inverse of the conversion forward in time.
        This view of converting backward in time also can be understood as
        converting forward through negative time. Thus it makes no distinction
        between P and F but rather treating both as being a value (P) relative
        to its corresponding time. This makes both P and F become instances of
        the same class where they will be treated as equivalent.
    """

    dateformat = '%d/%m/%Y'

    def __init__(self, value, date):
        """
        Initializes.

        @Params:
            - value: monetary ($)
            - date
        """
        self.value = float(value)
        self.originalDate = Date(date, TimeValue.dateformat)
        self.time = Date(date, TimeValue.dateformat) #self.date

    def __copy__(self):
        """
        Magic Method for the Shallow Copy Operation.
        Since this is a simple class this method functions as a deep copy.
        """
        timevalue = TimeValue(self.value, self.time)
        timevalue.originalDate = self.originalDate
        return timevalue

    def __str__(self):
        """
        Magic Method that returns a user-friendly representation of the object.
        """
        return 'Value: {} @ {}'.format(self.value, self.time.strftime(TimeValue.dateformat))

    def __validate__(self, other):
        """
        Provides an eazy reuse of code for operations
            that limit the "other" type they interact with.

        @Params:
            - other: the object that will be interacted with
        """
        if not isinstance(other, TimeValue):
            raise TypeError('TimeValue can only operate on TimeValue')
        if self.time != other.time:
            raise ValueError('Must have the same date!')
        maxoriginal = max(self.originalDate, other.originalDate)
        if self.time > maxoriginal:
            raise ValueError('Cannot convert beyond latest ({}) change in value!'.format(maxoriginal))

    def __add__(self, other):
        """
        Magic Method for implementing the addition (+) operator.
        Specifically the behaviour is to combine the values of
            this class's objects together when their times correlate.

        @Params:
            - other: the object that will be interacted with
        """
        self.__validate__(other)
        return TimeValue(self.value + other.value, self.time)

    def __sub__(self, other):
        """
        Magic Method for implementing the subtraction (-) operator.
        Specifically the behaviour is to combine the values of
            this class's objects together when their times correlate.

        @Params:
            - other: the object that will be interacted with
        """
        self.__validate__(other)
        return TimeValue(self.value - other.value, self.time)

    def __mul__(self, other):
        """
        Magic Method for implementing the multiplication (*) operator.
        Specifically the behaviour is to either combine an object of
            this class with a scalar or combine the values of this
            class's objects together when their times correlate.

        @Params:
            - other: the object that will be interacted with
        """
        if isinstance(other, (float, int)):
            return TimeValue(self.value * other, self.time)
        #if isinstance(other, Interest):
        #    return other.__rmul__(self)
        self.__validate__(other)
        return TimeValue(self.value * other.value, self.time)
    __rmul__ = __mul__

    def __truediv__(self, other):
        """
        Magic Method for implementing the multiplication (*) operator.
        Specifically the behaviour is to either combine an object of
            this class with a scalar or combine the values of this
            class's objects together when their times correlate.
        NOTE: for scalar values this is an ordered operation:
            <TimeValue object> / <scalar>

        @Params:
            - other: the object that will be interacted with
        """
        if isinstance(other, (float, int)):
            return TimeValue(self.value / other, self.time)
        self.__validate__(other)
        return TimeValue(self.value / other.value, self.time)
