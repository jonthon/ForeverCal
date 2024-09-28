#! python
from collections import deque
from datetime    import datetime


#######################################################################
# DEFAULTS (standard), customize how you want. See respective classes 
# to see how.
#######################################################################

# *YRDAYS are meant to be constant.
                     # number of days in a:
_COMMON_YRDAYS = 365  # common year
_LEAP_YRDAYS   = 366  # leap   year

# name = WEEKDAYS[index] default
# NOTE: 
#   data structures for customization; ie. names in different 
#   language or country or overall calendar 
_WEEKDAYS = ['Saturday',
             'Sunday',
             'Monday',
             'Tuesday',
             'Wednesday',
             'Thursday',
             'Friday',]

# MONTHDAYS[index - 1] => (name, days), mapper.
# Where, index is month number - 1. Leap month has two values 
# in a tuple; days = days[1] if yr_is_leap else days[0]
_MONTHDAYS =(['January',   (31,   )],
             ['February',  (28, 29)], # leap month
             ['March',     (31,   )],
             ['April',     (30,   )],
             ['May',       (31,   )],
             ['June',      (30,   )],
             ['July',      (31,   )],
             ['August',    (31,   )],
             ['September', (30,   )],
             ['October',   (31,   )],
             ['November',  (30,   )],
             ['December',  (31,   )],)


#########################################################################
# weekday formula, so cool
#########################################################################
def date_index(yrday, cmmnyrs, leapyrs, wkdays=_WEEKDAYS, 
                                        cmmnyrdays=_COMMON_YRDAYS, 
                                        leapyrdays=_LEAP_YRDAYS):
    """
    Returns an index of a date relative to its weekday name: 0 => Sat, 
    or 1 => Sun, or 5 = > Thu etc.
    
    args:
        yrday      => relative number of the date to its year
        cmmnyrs    => total common years from genesis date
        leapyrs    => total leap   years from genesis date
        wkdays     => number of days in a week        (default 7)
        cmmnyrdays => number of days in a common year (default 365)
        leapyrdays => number of days in a leap   year (default 366)
    """
    #
    #    cmmn      => total days of all common years since genesis date
    #    leap      => total days of all leap   years since genesis date
    #    total     => total days (leap + cmmn + yrday) since genesis

    # Formula breakdown:
    # --------------------------------------------------------------------
    # index = total % wkdays                                   ...(i)
    #          |
    #          v      
    # index = (cmmn + leap + yrday) % wkdays                   ...(i)
    #          |
    #          v
    # With modulus division distribution properties:
    # index = (cmmn  % wkdays + 
    #          leap  % wkdays + 
    #          yrday % wkdays ) % wkdays                       ...(i)
    # --------------------------------------------------------------------
    
    cmmn  = (cmmnyrs % wkdays) * (cmmnyrdays % wkdays)
    leap  = (leapyrs % wkdays) * (leapyrdays % wkdays)
    yrday = (yrday   % wkdays)
    total = sum(days % wkdays for days in (cmmn, leap, yrday))
    return  total % wkdays                      

def map_weekdays(name, index, wkdays=_WEEKDAYS):
    """
    This function derives a weekdays mapper relative to the 
    passed in name, index, and original mapper, wkdays. 
    Genesis dates use this interface. 
    """
    old = index - wkdays.index(name)
    new = deque(list(wkdays))
    new.rotate(old)
    return list(new)


########################################################################
# Year interfaces, have fun!
########################################################################
class Julian(int):
    """
    This is a year interface implemented with respect to the Julian 
    calendar. It's the base class to all year interfaces defined in 
    this module. 
    NOTE:
        LEAP_YRDAYS and CMMN_YRDAYS are used to get days in 
        year only, not the weekday of a date.
    """  
    LEAP_YRDAYS = _LEAP_YRDAYS
    CMMN_YRDAYS = _COMMON_YRDAYS

    def __new__(cls, year): return int.__new__(cls, year)

    def days(self):
        "returns total days of this year"
        if self.isleap(): return self.LEAP_YRDAYS
        return self.CMMN_YRDAYS

    def isleap(self):
        "returns a bool based on if year is leap or not"
        return self % 4 == 0

    def leapyrs(self):
        "returns total leap years between 0 and self, exclusively."
        return (self - 1) // 4 
    
    def cmmnyrs(self):
        "returns total common years between 0 and self, exclusively."
        return (self - 1) - self.leapyrs()

class Gregorian(Julian):
    """
    This is a year interface with respect to the Gregorian calendar. It 
    customizes isleap and leapyrs methods logic of the Julian class to 
    implement Gregorian calendar.
    """

    def isleap(self):
        isJulian = Julian.isleap(self)
        return (isJulian and self % 100 != 0) or (self % 400 == 0)

    def leapyrs(self):
        Julianyrs = Julian.leapyrs(self)
        return (Julianyrs) - (Julianyrs // 25) + (Julianyrs // 100)


########################################################################
# Month interfaces, how far can we go with customization?
########################################################################
class Month(int):
    """
    This is the base month interface. yr_is_leap (bool), also passed 
    along with month, tells if the year is leap or not; hence, it 
    returns the correct days of this month depending on if the year 
    is leap or not.
    
    MONTHDAYS is a ['name', (common, leap)] structure, where common and 
    leap are month days, respectively, based on whether subject year is 
    leap or not. leap is empty for non leap months. See global MONTHDAYS 
    for more. This structure preserves days in tuples such that only the 
    month names are customizable, not days. _MONTHDAYS is default.
    """
    MONTHDAYS = _MONTHDAYS

    def __new__(cls, month, yr_is_leap):
        self = int.__new__(cls, month)
        self.yr_is_leap = yr_is_leap
        return self

    def __str__(self):
        return self.name()        

    def days(self, monthdays=None):
        "returns total days of this month"
        mdays = self.MONTHDAYS if not monthdays else monthdays
        days  = mdays[self - 1][1]
        index = 1 if self.yr_is_leap and len(days) == 2 else 0
        return days[index]

    def priordays(self, monthdays=None):
        "returns total days prior to this month, exclusively"
        month = Month(1, self.yr_is_leap)
        days  = 0
        while month != self:        
            days  += month.days(monthdays)
            month += 1
            month  = Month(month, self.yr_is_leap)
        return days

    def name(self):
        "returns the name of this month"
        return self.MONTHDAYS[self - 1][0]


########################################################################
# Date Interface, the BEAST, the banger!!
########################################################################
class BasicDate:
    def __init__(self, year, month, day):
        self.year  = (Gregorian(year) 
                      if not isinstance(year, Julian) else year)
        self.month = (Month(month, self.year.isleap())
                      if not isinstance(month, Month) else month)
        self.day   = int(day)
        
    def yearday(self, monthdays=None):
        "returns the num of day in a year (default, 1 <= yd <= 366)."
        return self.month.priordays(monthdays) + self.day
    
    def weekday(self, genesis, **kwargs):
        return genesis.weekday(self.year, self.month, self.day, **kwargs)
        # you can literally pass Python's calendar module as genesis
        
class GenesisDate(BasicDate):
    "These dates can solve other dates' weekdays"
    WKDAYS      = _WEEKDAYS
    CMMN_YRDAYS = Gregorian.CMMN_YRDAYS
    LEAP_YRDAYS = Gregorian.LEAP_YRDAYS

    def __init__(self, year, month, day, weekday):
        BasicDate.__init__(self, year, month, day)
        self._wkday = weekday

    def map_weekdays(self, name, mapper):
        "returns an index => weekday name mapper for genesis mode"
        index = self.yearday() % len(mapper)
        return map_weekdays(name, index, mapper) 
    
    def weekday(self, y=None, m=None, d=None, **kwargs):
        """
        returns the weekday name; ie. Sun, Mon, Tue, ...etc.
        kwargs: 
            monthdays   => days in a month mapper
            name        => genesis weekday name 
            wkdays      => days in a week names mapper
            cmmnyrdays  => days in a common year
            leapyrdays  => days in a leap year
        """
        monthdays  = kwargs.get('monthdays')
        name       = kwargs.get('name',       self._wkday)
        wkdays     = kwargs.get('wkdays',     self.WKDAYS)
        cmmnyrdays = kwargs.get('cmmnyrdays', self.CMMN_YRDAYS)
        leapyrdays = kwargs.get('leapyrdays', self.LEAP_YRDAYS)
        date       = BasicDate(y, m, d) if all((y, m, d)) else self
        yrday      = date.yearday(monthdays)
        cmmnyrs    = date.year.cmmnyrs() - self.year.cmmnyrs()
        leapyrs    = date.year.leapyrs() - self.year.leapyrs()
        index      = date_index(yrday, cmmnyrs, leapyrs, len(wkdays), 
                                                         cmmnyrdays,
                                                         leapyrdays)
        return self.map_weekdays(name, wkdays)[index]
        
class Date(GenesisDate):
    """
    This is a hybrid (BasicDate and GenesisDate) date interface. 
    It embeds Gregorian and Month classes by default.
    
    Genesis dates protocol:
        A genesis date is a date with known weekday and can solve 
        other dates' weekdays. All Date objectd are genesis dates. 
        By default, today's date is the genesis unless a known 
        weekday is passed to Date.
        
    Examples:
        date1 = Date(Y, M, D, weekday)    # date1 is genesis
        date1.weekday(y, m, d)            # it can now derive
                                          # other dates' weekdays

        date2 = Date(Y, M, D)             # date2 is also genesis
        other.weekday()                   # it's weekday is derived
                                          # from today's date

        date3 = Date()                    # date3 is today's date
        date3.weekday(y, m, d)            # default genesis
    """
    def __init__(self, year=None, month=None, day=None, weekday=None):
        def today():
            today   = datetime.today()
            year    = today.year
            month   = today.month
            day     = today.day
            weekday = map_weekdays('Monday', 0)[today.weekday()]
            return year, month, day, weekday

        ymdw  = year, month, day, weekday
        if all(ymdw): 
            GenesisDate.__init__(self, year, month, day, weekday)
        elif all(ymdw[:-1]):
            genesis = GenesisDate(*today())
            weekday = genesis.weekday(year, month, day)
            GenesisDate.__init__(self, year, month, day, weekday)
        else:
            GenesisDate.__init__(self, *today())
    
# ditto to python calendar.weekday. 
# compatible as genesis with date.weekday(genesis, ...).
weekday = Date().weekday

##########################################################################
# week interfaces, here comes the presentation masterpiece!
##########################################################################
class PresentableDate(Date):
    def __str__(self):
        weekday = self.weekday() + ','
        month   = self.month.name()
        day     = str(self.day)
        year    = str(self.year)
        return ' '.join([weekday, month, day, year])

class PresentableMonth(Month):
    WKDAY1 = 'Sunday'
    WKDAYS = PresentableDate.WKDAYS

    def __new__(cls, *pargs, **kwargs):
        year, month = pargs[:2]
        year = Gregorian(year) if not isinstance(year, Julian) else year
        self = Month.__new__(cls, month, year.isleap())
        PresentableMonth.__init__(self, *pargs, **kwargs)
        return self
    
    def __init__(self, year, month):
        self.year   = year

    def __str__(self): 
        just, weeks = 3, []
        for week in list(self):
            days = self.repr_week(week, just)
            weeks.append(' '.join(days))
        names = map_weekdays(self.WKDAY1, 0, self.WKDAYS)
        names = [day[:just] for day in names]
        names = ' '.join(names)
        me    = self.name().center((just + 1) * len(week))
        weeks = [me, names] + weeks
        return '\n'.join(weeks)
    
    def __iter__(self):
        yield from self.my_weeks()

    def my_weeks(self, wkday1=None, **kwargs):
        wkday1       = self.WKDAY1 if not wkday1 else wkday1
        wkdays       = self.WKDAYS
        wkdays       = kwargs.get('wkdays', wkdays)
        days, names  = self.days_and_names(**kwargs)
        while len(names) > len(wkdays):
            last  = names.index(wkday1, 1)
            week  = days[:last]
            names = names[last:]
            days  = days[last:]
            yield self.restructure_week(week, -1, wkdays);
        else:
            yield self.restructure_week(days, 1, wkdays)

    def repr_week(self, week, just):
        days = []
        for day in week:
            day = str(day)
            day = day.replace(str(None), '')
            day = day.rjust(just)
            days.append(day)
        return days
    
    def days_and_names(self, **kwargs):
        weekday = PresentableDate().weekday
        days    = list(range(1, self.days() + 1))
        y, m    = self.year, self
        names   = [weekday(y, m, d, **kwargs) for d in days]  
        return days, names

    def restructure_week(self, week, side, wkdays): 
        empty = len(wkdays) - len(week)
        empty = [None] * empty 
        empty = empty + week if side < 0 else week + empty
        return empty

class PresentableYear:
    WKDAY1    = PresentableMonth.WKDAY1
    WKDAYS    = PresentableMonth.WKDAYS
    MONTHDAYS = PresentableMonth.MONTHDAYS
    def months(self, iterator=list):
        class Mth(PresentableMonth):
            WKDAY1    = self.WKDAY1
            WKDAYS    = self.WKDAYS
            MONTHDAYS = self.MONTHDAYS
        for m in range(len(Mth.MONTHDAYS)):
            m = Mth(self, m + 1) 
            m = iterator(m)
            yield m
    def __iter__(self):
        yield from self.months()
    def __str__(self): 
        temp = str(int(self))
        temp = temp.center(len(self.WKDAYS) * 4)
        return (temp + '\n') + '\n\n'.join(self.months(str))

class PresentableJulian(Julian,       PresentableYear): pass

class PresentableGregorian(Gregorian, PresentableYear): pass 

#####################################################
# Top Level code
#####################################################
if __name__ == '__main__':
    import unittest, sys
    import calendar
    from forevercal import (PresentableGregorian as Year, 
                            PresentableMonth     as Month, 
                            PresentableDate      as Date)

    names = map_weekdays('Monday', 0, _WEEKDAYS)
    
    def verbose(y):
        if verbosity and y % 100 == 1: 
            print('century:', y // 100 + 1) # current century
        
    def itermonth(tester, genesis, y):
        months = range(1, 12 + 1, 1)
        for m in months:
            m       = Month(y, m)                  
            genesis = iterdays(tester, genesis, y, m)
            return genesis
        
    def iterdays(tester, genesis, y, m):
        days = range(1, m.days() + 1, 1)
        for d in days:
            my_wkday = genesis.weekday( y, m, d)
            py_wkday = calendar.weekday(y, m, d)
            py_wkday = names[py_wkday]
            tester.assertEqual(my_wkday.lower(), py_wkday.lower()) # test
            genesis  = Date(y, m, d, my_wkday)
            return genesis

    class ForeverCalTests(unittest.TestCase):
        def setUp(self): print()

        def testWeekday(self):
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
            genesis = Date(end, 1, 1) if end else Date() # true genesis, 
            years   = range(1, genesis.year + 1, 1)                              
            for y in years:
                verbose(y)
                y       = Year(y)                                    
                genesis = itermonth(self, genesis, y)
    verbosity = True if sys.argv[1] == '-v' else False
    try:
        end = sys.argv.pop(2)
    except:
        end = datetime.today().year
    unittest.main()
