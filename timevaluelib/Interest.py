"""
@THEORY:
According to Economical Theory, money on hand is more valuable than
money lent out to others because it results in the loss of opportunity
that is brought on by being able to make an immediate payment (NOTE: there
do exist non-monetary opportunities but since money has the ability to
take advantage of almost every opportunity they are deemed insignificant
and ignored). As a result, in order to balance this cost of lending, the
lendee is required to pay compensation for this opportunity loss during
the payback of the load, which is called Interest. Usually this interest
is expressed as a rate called the Interest Rate.

Compound Interest happens when the interest is repeated over many subperiods.
(See TimeValue module docstring for equations). The Nominal Interest (r) is
the stated interest for the full period for which the subperiods comprise.
Effective Interest is the equivalent interest (as though not compounding)
that results from compounding on the subperiods:
    ieffective = r / m where m is the number of subperiods.
The Effective Interest is the actual interest you pay and is not usually stated.
Typically an interest compounds annually but does not have to be.

##PLACEHOLDER for when include Annities##

Since physical material breaks down, Governments continuously must print new money
to replace the worn money. In addition, Governments can control the amount of money
in circulation by introducing more or less new money than the old they remove. This
is done for many reasons (not covered in this module) and has many business impacts.
The major business impact comes from the resulting inflation or deflation. Since the
"value" or "buying power" of money is determined by the amount you have relative to
the amount others have, the introduction of more into circulation decreases the value
(inflation) and the introduction of less into circulation increases the value (deflation).

It is worse to have deflation (not covered in this module) and generally accepted
to be impossible to have neither inflation or deflation; as a result many countries
choose to impose a certain amount of predetermined inflation on their Economy.
The result of inflation on interest is that it decreases the value of the compensation
(interest) and so effectively reduces the interest rate -- NOTE: the interest rate
stated is not the effectively reduced interest rate but the rate before inflation.
"""

from datetime import timedelta as TimeSpan

from timevaluelib.TimeValue import TimeValue

class Interest(object):
    """
    Class for representing interest (compounded or not).

    Specifically objects of this class use an interest rate to calculate
        value conversions through time. This conversion is needed for
        comparing between the value of the money on hand (including its
        opportunity) with the value of the money once the lender has paid
        back the loan (including the interest). This means that the value
        of the money (the amount) on hand is treated as equivalent to the
        amount loaned plus the interest (as the interest is only there to
        compensate for opportunity and not add to the value of the money).
    """

    def __init__(self, rate, period, subperiod=None):#, start, finish=None):
        """
        Initializes.

        @Params:
            - rate: interest rate (nominal rate -- full period)
            - period: interest period; length of time between interest payments
            - subperiod: number of compoundings within a period
        """
        self.rate = float(rate)
        self.period = period if isinstance(period, TimeSpan) else TimeSpan(period)
        self.subperiod = int(subperiod) if subperiod else None
        if self.subperiod:
            self.effectiveRate = (1 + self.rate / self.subperiod)**self.subperiod - 1
        else:
            self.effectiveRate = self.rate
        #self.start = DateTime(start)
        #self.finish = DateTime(finish) if finish else DateTime('Today')

    def convert(self, deltaperiods):
        """
        Calculates a ratio that converts any value across a change (delta) in time.
            This time-conversion calculation is independent of when the start
            and finish of any conversion is.

        WARNING: Use of this method directly with TimeValue causes integrity
            issues as it does not modify the TimeValue time so the "conversion"
            would simply change the value at the time it would originally be at.
            This means that its value relative to its time would change (impossible)
            and you would be gaining or losing time-value amounts instead of
            comparing the same time-value amount across times with different values.

        @Params:
            - deltaperiods: the change (delta) in time to convert through
        """
        #deltaperiods and self.period relationship
        return (1 + self.effectiveRate)**deltaperiods

    def __str__(self):
        """
        Magic Method that returns a user-friendly representation of the object.
        """
        return 'Interest Rate: {}\nInterest Period: {}\nSubperiods: {}'.format(self.rate, self.period, self.subperiod)

    def __pow__(self, deltaperiods):
        """
        Magic Method for implementing the exponential/power (**) operator.
        Specifically the behaviour combines self.convert with a time conversion.
        """
        return Interest(rate=self.convert(deltaperiods)-1, period=deltaperiods*self.period)

    def __rmul__(self, timevalue):
        """
        TEMPORARILY: a single multiply represents a single period jump forward in time.
        """
        timevalue = timevalue.__copy__()
        timevalue.value *= self.convert(1)
        timevalue.time += self.period
        return timevalue

    def __rdiv__(self, timevalue):
        """
        TEMPORARILY: a single divide represents a single period jump backward in time.
        """
        timevalue = timevalue.__copy__()
        timevalue.value /= self.convert(1) #timevalue.value *= self.convert(-1)
        timevalue.time += self.period
        return timevalue

_originalTVmul = TimeValue.__mul__
def _TVmulI(self, interest):
    """
    TEMPORARILY: a single multiply represents a single period jump forward in time.
    """
    if isinstance(interest, Interest):
        timevalue = self.__copy__()
        timevalue.value *= interest.convert(1)
        timevalue.time += interest.period
        return timevalue
    else:
        return _originalTVmul(self, interest)
setattr(TimeValue, '__mul__', _TVmulI)
setattr(TimeValue, '__rmul__', _TVmulI)

_originalTVdiv = TimeValue.__truediv__
def _TVdivI(self, interest):
    """
    TEMPORARILY: a single divide represents a single period jump backward in time.
    """
    if isinstance(interest, Interest):
        timevalue = self.__copy__()
        timevalue.value /= interest.convert(1) #timevalue.value *= interest.convert(-1)
        timevalue.time += interest.period
        return timevalue
    else:
        return _originalTVdiv(self, interest)
setattr(TimeValue, '__truediv__', _TVdivI)
