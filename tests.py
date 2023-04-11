
import unittest
from datetime import datetime
from forevercal import (Date, Gregorian as Greg, Month, 
                        OutOfRange)

class ForeverCalTests(unittest.TestCase):
    def setUp(self): print()
    
    def test_date_attrs(self):
        today   = datetime.today()
        y, m, d = today.year, today.month, today.day
        date = Date(y, m, d)
        for values in zip([date.year, date.month, date.day], 
                          [y, m, d]):
            self.assertEqual(*values)
        def func(n): date.year = n
        self.assertRaises(Exception, func, 0)

    def test_in_range(self):
        """
        Testing if the values passed are in range.

        In these, year = 0, month = 0 or 13, day = 0 or 32.
        """
        self.assertRaises(OutOfRange, Greg,  0)             # year  = 0
        self.assertRaises(OutOfRange, Month, 0,  False)     # month = 0
        self.assertRaises(OutOfRange, Month, 13, False)     # month = 13
        self.assertRaises(OutOfRange, Date,  1, 1, 0)       # day   = 0
        self.assertRaises(OutOfRange, Date,  1, 1, 32)      # day   = 32
        
    def test_yrdays(self):
        "testing if common and leap years are right"
        self.assertEqual(Greg(4).days(), 366)
        self.assertEqual(Greg(5).days(), 365)


    def test_weekday(self):
        """
        Testing if forevercal weekday == pyhton weekday.
        All core interfaces for Julian, Month, and Date
        are used implicitly (Gregorian is used).
        
        Each derived date derives the next date's weekday

        -v CLI arg enables test verbosity. It prints
        current century year tested.

        This is the core test. If this fails, nothing 
        else in the interface matters.
        """
        import calendar
        
        today = datetime.today()
        date  = Date(today.year, today.month, today.day,
                    ['Monday', 
                     'Tuesday', 
                     'Wednesday', 
                     'Thursday', 
                     'Friday', 
                     'Saturday', 
                     'Sunday'][today.weekday()])     # true genesis

        # test logic
        century = 1                              
        for y in range(1, datetime.today().year + 1, 1):

            # -v (verbosity)
            if verbose and ((y < 100 and century == 1) or 
                            y % 100 == 1):
                print('century:', century)
                century += 1

            Y = Greg(y)                                    # year
            for m in range(1, 12 + 1, 1):
                M = Month(m, Y.isleap())                   # month
                for d in range(1, M.days() + 1, 1):
                    date       = date(y, m, d)             # date
                    fc_weekday = date.weekday()
                    # fc_weekday = date.weekday(y, m, d)   # alt
                    py_weekday = calendar.weekday(y, m, d)
                    py_weekday = ['Monday',                # weekday
                                'Tuesday',                 # names
                                'Wednesday',
                                'Thursday',
                                'Friday',
                                'Saturday',
                                'Sunday'][py_weekday]
                    # test operation
                    self.assertEqual(
                        fc_weekday.lower(), py_weekday.lower())

if __name__ == '__main__':
    import sys
    verbose = True if '-v' in sys.argv else False
    unittest.main()
