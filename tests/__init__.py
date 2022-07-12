
import timevaluelib
timevaluelib.DATE_FORMAT = '%d/%m/%Y'

import tests
from tests.interest_tests import InterestTests
from tests.timevalue_tests import TimeValueTests
from tests.examples import TimeValueLibExamples

__all__ = ['InterestTests', 'TimeValueTests', 'TimeValueLibExamples']
