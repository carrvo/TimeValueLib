import unittest

from timevaluelib import TimeValue,Interest

class TimeValueLibExamples(unittest.TestCase):

    def test_operations_example(self):
        firstyear = Interest(rate=0.1, period=365) # 10% for 1 year
        secondyear = Interest(0.2, 365, 12) # 20% for 1 year compounded monthly
        start = TimeValue(500, '01/01/0001') # $500 day 1 of month 1 of year 1
        firstpayment = TimeValue(-100, '01/01/0002') # pay $100 year 2
        firstearning = TimeValue(50, '01/01/0002') # earn $50 year 2
        secondpayment = TimeValue(-100, '01/01/0003') # pay $100 year 3
        secondearning = TimeValue(50, '01/01/0003') # earn $50 year 3

        # cannot add when different dates
        self.assertRaises(ValueError, lambda: start + firstpayment)
        # convert using interest then add
        self.assertEqual(str(firstyear * start + firstpayment), 'Value: 450.0 @ 01/01/0002')
        # conversion using interest
        self.assertEqual(str(firstyear * start), 'Value: 550.0 @ 01/01/0002')
        # many additions
        self.assertEqual(str(firstyear * start + firstpayment + firstearning), 'Value: 500.0 @ 01/01/0002')
        # store conversion in new variable
        firstamount = firstyear * start + firstpayment + firstearning
        # confirm storage
        self.assertEqual(str(firstamount), 'Value: 500.0 @ 01/01/0002')
        # store conversion
        secondamount = secondyear * firstamount + secondpayment + secondearning
        # confirm storage
        self.assertEqual(str(secondamount), 'Value: 559.6955424526158 @ 01/01/0003')
        # multiplicable with scalars
        self.assertEqual(str(5 * secondamount), 'Value: 2798.477712263079 @ 01/01/0003')
        # order does not matter
        self.assertEqual(str(secondamount * 5), 'Value: 2798.477712263079 @ 01/01/0003')
        # order does not matter for interest either
        secondamount = firstamount * secondyear + secondpayment + secondearning
        self.assertEqual(str(secondamount), 'Value: 559.6955424526158 @ 01/01/0003')
        # subtractable too
        secondamount = firstamount * secondyear + secondpayment - secondearning
        self.assertEqual(str(secondamount), 'Value: 459.69554245261577 @ 01/01/0003')
        # print object to screen
        self.assertEqual(str(secondyear), 'Interest Rate: 0.2\nInterest Period: 365 days, 0:00:00\nSubperiods: 12')
        # ratio for 1 year ahead (supports negatives for backward)
        self.assertEqual(secondyear ** 1, 1.2193910849052316)
        # ratio for 10 years ahead
        self.assertEqual(secondyear ** 10, 7.26825499216019)

        self.assertRaises(TypeError, lambda: secondpayment / secondyear)
        self.assertRaises(TypeError, lambda: secondyear / secondpayment)
        self.assertRaises(TypeError, lambda: secondpayment / secondearning)
        self.assertRaises(TypeError, lambda: secondpayment / 5)
        #supposed to support division...

        self.assertEqual(str(secondpayment * 5), 'Value: -500.0 @ 01/01/0003')
        # support multiplication
        self.assertEqual(str(secondpayment * secondearning), 'Value: -5000.0 @ 01/01/0003')
        self.assertEqual(str(firstearning * firstyear), 'Value: 55.00000000000001 @ 01/01/0003')
        # order does not matter
        self.assertEqual(str(firstyear * firstearning), 'Value: 55.00000000000001 @ 01/01/0003')
        # multiplication must also have same date
        self.assertRaises(ValueError, lambda: firstearning * secondearning)
        # convert and multiply
        self.assertEqual(str(firstearning * firstyear * secondearning), 'Value: 2750.0000000000005 @ 01/01/0003')
        # convert and add
        self.assertEqual(str(firstearning * firstyear + secondearning), 'Value: 105.0 @ 01/01/0003')
        # convert and add then convert again
        self.assertEqual(str((firstearning * firstyear + secondearning) * secondyear), 'Value: 128.0360639150493 @ 01/01/0004')
