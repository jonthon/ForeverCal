
#######################################################################
#   DEFAULTS (standard), customize how you want. See respective classes 
# to see how.
#######################################################################

# *YRDAYS are meant to be constant
                      # number of days in a:
_COMMON_YRDAYS = 365  # common year
_LEAP_YRDAYS   = 366  # leap   year

# default WEEKDAYS[index] => name, mapper
#             ||
#             vv
# NOTE: data structures for customization; ie. names in different 
# language or country or overall calendar (see also Month.MONTHDAYS)
#
# name = WEEKDAYS[index] 
WEEKDAYS = ['Saturday',
            'Sunday',
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',]

# MONTHDAYS[index - 1] => (name, days), mapper
#                ||
#                vv
# where index is month number - 1 leap month has two values in a tuple, 
# where days = days[1] if yr_is_leap else days[0]
MONTHDAYS =(['January',   (31,   )],
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
def calendar_ix(yrday, c_yrs, l_yrs, *, wkdays, 
                c_yrdays=_COMMON_YRDAYS, l_yrdays=_LEAP_YRDAYS):
    """
    Returns index of a date relative to calendar. See Date class 
    implementation for use case.

    --------------------------------------------------------------------
    Formula breakdown:
            |
            v
    index = total % wkdays                                   ...(i)
            |
            v      
    index = (cmmn + leap + yrday) % wkdays                   ...(i)
            |
            v
    With modulus division distribution properties:
    index = (cmmn  % wkdays + 
             leap  % wkdays + 
             yrday % wkdays ) % wkdays                       ...(i)
                
    Formula variables:
        cmmn     => total days of all common years since genesis day
        leap     => total days of all leap   years since genesis day
        yrday    => number of the subject day relative to its year
        wkdays   => number of days in a week
        total    => total days (leap + cmmn + yrday) since genesis
        
    args:
        yrday    => (see Formula variables section)
        c_yrs    => total number of common years since genesis
        l_yrs    => total number of leap   years since genesis
        wkdays   => (see Formula variables section)
        c_yrdays => number of days in a common year
        l_yrdays => number of days in a leap   year
        
    --------------------------------------------------------------------
    """
    cmmn  = (c_yrs % wkdays) * (c_yrdays % wkdays)
    leap  = (l_yrs % wkdays) * (l_yrdays % wkdays)
    yrday = (yrday % wkdays)
    total = sum(map(lambda n: n % wkdays, (cmmn, leap, yrday)))
    return  total % wkdays                      



# it's made implicit accross multiple class namespaces, 
# (so global name), see Date and Week. In short, it's for
# reuse.
def map_weekdays(weekday, weekday_ix, weekdays):
    """
    This function derives an index => weekday name mapper relative to 
    the passed in arguments. Genesis dates use this interface to derive 
    a global weekday mapper. 
    
    args:
        weekday    => genesis weekday name
        weekday_ix => genesis weekday index
        weekdays   => weekday names
    """
    total      = len(weekdays)
    old_wkdays = weekdays
    new_wkdays = [None] * total
    new_ix     = weekday_ix
    old_ix     = old_wkdays.index(weekday)
    for i in range(total):                           # rotate in old
        old_ix = (old_ix + 1) % total                # and reflect in new
        new_ix = (new_ix + 1) % total           
        new_wkdays[new_ix] = old_wkdays[old_ix] 
    return new_wkdays



########################################################################
# Custom Exceptions (for better control flow)
########################################################################
class OutOfRange(Exception):
    """
    Checks if num is in the expected range. Users are expected to 
    customize the in_range method to return True for satisfaction and 
    False if otherwise (raises exception implicitly). See Julian, Month, 
    and Date classes for use cases.
    """
    
    range_str = ''
    
    def __init__(self, num):
        if not isinstance(num, int):
            raise TypeError('[<int> required]')
        msg  = 'value not in range: %s' 
        msg %= self.range_str
        Exception.__init__(self, msg)
        if not self.in_range(num): raise self
        
    def in_range(self, num):
        # customize in respective classes.
        pass

class DateNotGenesis(Exception):
    """
    raised when a non genesis date is misused to derive another date's 
    weekday. Any date can be a genesis date but has to follow the 
    protocol of explicitly specifying it's own weekday name or be 
    derived from an explicit genesis date.
    """
    def __init__(self):
        Exception.__init__('[operation is for genesis dates only]')



########################################################################
# Year interfaces, have fun!
########################################################################
class Julian:
    """
    This is a year interface implemented with respect to the Julian 
    calendar. It's the base class to all year interfaces defined in this 
    module. 
    
    Raises Verify (OutOfRange subclass) defined in this class's scope 
    for an invalid year arg.
    """
    
    class Verify(OutOfRange):
        range_str = 'yr > 0'
        def in_range(self, yr):
            return yr > 0
            
    def __init__(self, year):
        self.Verify(year)
        self.y = year

    def __repr__(self):
        return '%s(%d)' % (self.__class__.__name__, self.y)

    def days(self):
        "returns total days of this year"
        if self.isleap():
            return _LEAP_YRDAYS
        return _COMMON_YRDAYS

    def isleap(self):
        "returns a bool based on if year is leap or not"
        self.Verify(self.y)
        return self.y % 4 == 0

    def years_between(self, other):
        "returns total (leap, common) years, max(self, other) inclusive"      
        
        # TBD:
        # include negative signs for years lower than start year?
        y1 = self.y
        y2 = other
        
        if y1 == y2: return 0, 0             # same year, no difference.
        
        Year = self.__class__
        
        t1 = Year(y1).all_years()
        t2 = Year(y2).all_years()
        lyrs = t2[0] - t1[0]
        cyrs = t2[1] - t1[1]
        return lyrs, cyrs 

    def all_years(self):
        "returns total (leap, common) between 0 and self.y, exclusively"    
        lyrs = self.leap_years()
        cyrs = (self.y - 1) - lyrs
        return lyrs, cyrs                   # total (leap, common) tuple

    def leap_years(self):
        "returns total leap years between 0 and self.y, exclusively."
        self.Verify(self.y)
        return (self.y - 1) // 4 

    # May not be customizable coz logic is not proved.
    # But it works with defaults: WEEKDAYS, C_YRDAYS, L_YRDAYS, ...etc
    def twin_years(self, other, *, wkdays, diff):
        "yields repeating years inclusively on demand"
        Year = self.__class__
        yr, y2 = sorted([self.y, other])
        yield yr                              # yield own first
        while True:
            twin = yr + wkdays
            lyrs = Year(yr - 1).years_between(twin - 1)[0]
            twin -= lyrs
            if lyrs == diff and Year(twin).isleap():
                yr   = twin
                twin = yr + wkdays
                lyrs = Year(yr).years_between(twin - 1)[0]
                twin -= lyrs
            yr = twin
            if yr > y2: return
            if Year(yr).days() == self.days(): yield yr


class Gregorian(Julian):
    """
    This is a year interface with respect to the Gregorian calendar. It 
    only customizes isleap and leap_years methods logic of the Julian 
    class to implement Gregorian calendar.
    """

    def isleap(self):
        is_julian = Julian.isleap(self)
        return (is_julian and self.y % 100 != 0) or (self.y % 400 == 0)

    def leap_years(self):
        lyrs = Julian.leap_years(self)
        return (lyrs) - (lyrs // 25) + (lyrs // 100)



########################################################################
# Month interfaces, how far can we go with customization?
########################################################################
class Month:
    """
    This is the base month interface. It takes a valid month (int) arg 
    that satisfies 1 <= month <= 12 or Verify (OutOfRange subclass) is 
    raised. is_yr_leap (bool), also passed along with month, tells if 
    the year is leap or not; hence, it returns the correct days of this 
    month depending on if the year is leap or not.
    
    MONTHDAYS is a ['name', (common, leap)] structure, where common and 
    leap are month days respectively based on whether subject year is 
    leap or not. leap is empty for non leap months. See global MONTHDAYS 
    for more. This structure preserves constants in tuples such that 
    only the month names are customizable, by in place change operations; 
    custom language month names.
    """
    from copy import deepcopy
    MONTHDAYS = deepcopy(MONTHDAYS)
            
    def __init__(self, month, is_yr_leap):
        
        # in local scope so as to reference self, hence, MONTHDAYS
        class Verify(OutOfRange):
            range_str = "1 <= mth <= %d" % len(self.MONTHDAYS)
            def in_range(verify, mth):
                return 1 <= mth <= len(self.MONTHDAYS)
        self.Verify     = Verify
        
        self.Verify(month)
        self.m          = month
        self.yr_is_leap = is_yr_leap

    def __repr__(self):
        return '%s(%d, %s)' % (self.__class__.__name__, 
                               self.m, 
                               self.yr_is_leap)

    def days(self):
        "returns total days of this month"
        days  = self.MONTHDAYS[self.m - 1][1]
        index = 1 if self.yr_is_leap and len(days) == 2 else 0
        return days[index]
            
    def prior_days(self):
        "returns total days prior to this month, exclusively"
        month = self.__class__(1, self.yr_is_leap)
        days  = 0
        while month.m != self.m:        
            days    += month.days()
            month.m += 1
        return days

    def name(self):
        "returns the name of this month"
        self.Verify(self.m)
        return self.MONTHDAYS[self.m - 1][0]


########################################################################
# Date Interface, the BEAST, the banger!!
########################################################################
class Date:
    """
    
    This is the base date interface. It embeds Gregorian and Month 
    classes by default; they are assigned in this class's local scope, 
    customize as desired.
    
    year, month, and day attrs are for referencing, not reassigning y, m, 
    and d respectively.
    
    WEEKDAYS is a Date's attr that holds default weekday names. Ideal 
    for custom language weekday names, customize as desired.
    
    Genesis date protocol:
        A genesis date is any date with a known weekday name. Thus, they 
        can derive other dates' weekday names.
        
    Example usage:
        date  = Date(Y, M, D, weekday)    # genesis date
        other = date(y, m, d)             # other   date
        # to get weekday name
        try:
            wday = other.weekday()
        #        OR
        #   wday = date.weekday(y, m, d)
        except DateNotGenesis:
            # weekday raises this exception if weekday is 
            # not determined or specified.
            ...
        else:
            # if everything goes well, you get the weekday name 
            # of the subject date.
            # Thus, date, other, and other dates derived from 
            # these are all genesis themselves.
            ...
    
    """
    Year     = Gregorian
    Month    = Month
    WEEKDAYS = list(WEEKDAYS)
    
    # for convenience
    class Attr:
        def __init__(attr, name):
            attr.name = name
        def __get__(attr, date, Date):
            if   attr.name == 'year':  return date.y.y
            elif attr.name == 'month': return date.m.m
            elif attr.name == 'day':   return date.d
        def __set__(*pargs, **kwargs):
            raise Exception('[operation not supported]')      
    year  = Attr('year')
    month = Attr('month')
    day   = Attr('day')

    def __init__(self, y, m, d, genesis_weekday=None):
        self.y = self.Year(y)
        self.m = self.Month(m, self.y.isleap())
        
        # in local scope so as to reference self
        class Verify(OutOfRange):
            range_str = "0 <= day <= %d" % self.m.days()
            def in_range(verify, day):
                return 1 <= day <= self.m.days()
        self.Verify = Verify
        
        self.Verify(d)
        self.d = d
        if genesis_weekday: self._weekday = genesis_weekday
        
    def __gt__(self, date):
        "returns True if date is later, otherwise False"
        y1, m1, d1 = self.y.y, self.m.m, self.d         # explicit names
        y2, m2, d2 = date.y.y, date.m.m, date.d         # for readability

        return ((y1 >  y2) or                           # check years
                (y1 == y2 and m1 >  m2) or              # then months
                (y1 == y2 and m1 == m2 and d1 > d2))    # finally days

    def __ge__(self, date):
        "returns True if date is later or equal to self, otherwise False"
        islatter = self > date
        return islatter or (islatter and self.d == date.d)
    
    def __call__(genesis, *pargs, **kwargs):
        """
        Derives the weekday of a customized Date instance, and returns a 
        Date instance with known weekday (genesis).
        """
        # CustomDate is nested to remember genesis from enclosing 
        # __call__ scope in calendar_ix local scope and not in instance 
        # (date) namespace. If it aint simple, use other way; ie. 
        # namespace, scope, etc
        Genesis = genesis.__class__
        class CustomDate(Genesis):
            def calendar_ix(date):
                yrday = abs(date.yearday())
                yrs   = genesis.y.years_between(date.y.y)
                return calendar_ix(yrday, yrs[1], yrs[0],
                                   wkdays=len(genesis.WEEKDAYS)) 
            def weekdays(date): return genesis.weekdays()     
        genesis_weekday = CustomDate(*pargs, **kwargs).weekday()
        return Genesis(*pargs[:3], genesis_weekday, **kwargs);

    def yearday(self):
        "returns the num of day in a year (default, 1 <= yd <= 366)."
        self.Verify(self.d)
        return self.m.prior_days() + self.d

    def weekdays(self):
        "returns an index => weekday name mapper for genesis mode"
        try:
            return map_weekdays(self._weekday,                      
                               self.yearday() % len(self.WEEKDAYS),  
                               self.WEEKDAYS)                        
        except AttributeError:
            raise DateNotGenesis
                                                                              
    def calendar_ix(self):
        "returns the index of this date relative to calendar"
        return self.yearday() % len(self.WEEKDAYS)
        
    def weekday(self, y=None, m=None, d=None):
        "returns the weekday name; ie. Sun, Mon, Tue, ...etc."
        # return own weekday 
        if not (y and m and d): return self.weekdays()[self.calendar_ix()]
        # or return (y, m, d) weekday
        return self(y, m, d, None).weekday()

class PresentableDate(Date):
    def __str__(self):
        return (self.weekday() + ', ' + 
                self.m.name()[:3:] + ' ' + 
                str(self.d) + ' ' + str(self.y.y))



##########################################################################
# week interfaces, here comes the presentation masterpiece!
##########################################################################
class Week:
    "Week instances yield weeks on demand based on provided args"
    def __init__(self, start_weekday, start, stop, *, 
                 weekday1, weekdays):
        "Reusable interface that generates str() a month"
        self.mapper = map_weekdays(weekday1, 0, weekdays)
        self.index  = self.mapper.index(start_weekday)
        self.start  = start
        self.stop   = stop

    def __iter__(self):
        yield from self.__week(self.index, self.start, self.stop)

    def __week(self, index, start, stop):
        week = [0] * len(self.mapper)
        for day in range(start, stop + 1):
            if not index % len(week) and any(week):
                yield tuple(week)
                week = [0] * len(self.mapper)
            week[index % len(week)] = day
            index += 1
        else:
            yield tuple(week)

    def __str__(self):
        # could improve logic to suit longer weekday names
        names = ' '.join([n[:3].capitalize() for n in self.mapper])
        clean = lambda d: ' %s' % str(d).ljust(2) if d else '   '
        weeks = [' '.join(map(clean, w)) for w in self]
        return '\n'.join([names] + weeks)

class PresentableMonth(Month, Week):
    def __init__(self, m, is_yr_leap, day1_weekday, *, 
                 weekday1=None, weekdays=None, monthdays=None):
        # assign defaults if values not passed:
        weekday1  = 'Sunday'       if not weekday1 else weekday1
        weekdays  = list(WEEKDAYS) if not weekdays else weekdays
        if monthdays:
            # change month names in place
            for index, monthname in enumerate(monthdays):
                self.MONTHDAYS[index][0] = monthname
        # customize to make it Presentable
        Month.__init__(self, m, is_yr_leap)
        Week.__init__(self, day1_weekday, 1, self.days(), 
                      weekday1=weekday1, weekdays=weekdays)
                      
     # Month presentation logic.
     # Implicitly applied in the Presentable* classes
    def __str__(self):
        name = ''.ljust(10) + self.name().ljust(5) + '\n' 
        return name + Week.__str__(self) + '\n\n'

def PresentableYear(YearType):
    "Year type wrapper"
    class _PresentableYear(YearType):
        def __init__(self, y, day1_weekday, **kwargs):
            YearType.__init__(self, y)
            
            # customizes PresentableMonth for simplicity:
            # **kwargs are passed once and not on each call.
            # Also reused in __iter__.
            class DisplayMonth(PresentableMonth):
                def __init__(self, m, is_yr_leap, 
                             day1_weekday=day1_weekday):
                    PresentableMonth.__init__(self, m, is_yr_leap, 
                                              day1_weekday, **kwargs)
            # customizes Date to keep Date features in sync:
            # Year, Month, WEEKDAYS
            class DisplayDate(PresentableDate):
                Year  = YearType
                Month = DisplayMonth
                if 'weekdays' in kwargs: WEEKDAYS = kwargs['weekdays']
                
            self.DisplayMonth = DisplayMonth
            self.date         = DisplayDate(self.y, 1, 1, day1_weekday)
        
        # reuses self.DisplayMonth to append each month str()
        def __iter__(self):
            self._str = ''          # for reuse in self.__str__()
            for M, ignore in enumerate(self.DisplayMonth.MONTHDAYS, 1):
                yield (M,)          # yield month name first, then days
                weekday1 = self.date.weekday(self.y, M, 1)
                m = self.DisplayMonth(M, self.isleap(), weekday1)
                self._str += str(m) # append month str() 
                yield from m
                
        def __str__(self):
                        # year num + year days grouped by months
            list(self);
            return ''.ljust(12) + str(self.y) + '\n' + self._str
            
    def twin_years(self, other, *, weekdays=list(WEEKDAYS), diff=2):
        YearType.twin_years(self, other, wkdays=weekdays, diff=diff)

    return _PresentableYear

@PresentableYear
class PresentableJulian(Julian):       pass

@PresentableYear
class PresentableGregorian(Gregorian): pass

#####################################################
# Top Level code
#####################################################
if __name__ == '__main__':
    from argparse import ArgumentParser
    from datetime import datetime
    
    # CLI args
    parser = ArgumentParser()
    parser.add_argument('-y', type=int, help='year, prints the year.')
    parser.add_argument('-m', type=int, help='month, prints the month.')
    parser.add_argument('-d', type=int, help='day, prints the day.')
    args = parser.parse_args()
    y, m, d = args.y, args.m, args.d
    
    today = datetime.today()
    date  = PresentableDate(today.year, today.month, today.day,
                # hard coded python weekday index mapper
                ['Monday',
                 'Tuesday', 
                 'Wednesday', 
                 'Thursday', 
                 'Friday', 
                 'Saturday', 
                 'Sunday'][today.weekday()])
    
    # print year
    if y and m and d:
        print(date(y, m, d))
        
    # print month
    elif y and m:
        wday1  = date(y, m, 1).weekday()
        isleap = Gregorian(y).isleap()
        print(PresentableMonth(m, isleap, wday1))
        
    # print date
    elif y:
        wday1 = date(y, 1, 1).weekday()
        print(PresentableGregorian(y, wday1))
    elif y:
        wday1 = date(y, 1, 1).weekday()
        print(PresentableGregorian(y, wday1))
    
