import unittest

import sys
import os
sys.path.append(os.path.abspath(os.curdir))

import test
from interest_tests import InterestTests
from timevalue_tests import TimeValueTests
from examples import TimeValueLibExamples

unittest.main()
