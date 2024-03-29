# ForeverCal


NAME:
-----

``forevercal`` is named after forever calendar. It determines a weekday of any date of any given year.


MOTIVE:
-------

The main motive of this module is to improve explicitness from the built-in python weekday interface (``calendar.weekday``). 

Python weekday hardcodes its index => weekday mapper: 0 => 'Mon', 1 => 'Tue', 2 => 'Wed', ... etc. Compared to this module, that mapper is True for genesis date 1/1/1. However, this module offers more flexibility to specify a custom genesis date (Yes, even today) with args ``(y, m, d, weekday)`` to ``*Date`` interfaces. The genesis date derives a new mapper that's compatible with any specified subject date (even earlier than the genesis date). However, it only works for any given year > 0.


DESCRIPTION:
------------

This module implements an algorithm for determining the weekday (Sun, Mon, Tue, ... etc) of any date given a known weekday of a prime date (genesis date). The algorithm was developed by the author of this module from scratch and tested locally, see the top level code in this file.

``Presentable*`` classes are the recommended interfaces to use because they are the highest level interfaces, easy to use, and follow a simplicity approach. They are also reusable to various front ends: console, GUI, Web, ... etc. They define ``__str__`` for printing. ``Presentable*`` month and year interfaces define ``__iter__`` which makes them iterable, yielding weeks on demand. Ideal for use in GUI and Web frontends since ``__str__`` may not be suitable.

Values passed to the year, month, and date interfaces of this module are validated. For instance, invalid year, month, and day values raise ``OutOfRange`` instances if they are out of expected range (see their respective classes code for implementation). However, users should remember to handle these errors for better flow management. 

Documentation: https://forevercal.readthedocs.io/en/latest/


EXAMPLES:
--------
- ``PresentableGregorian`` interface (``PresentableJulian`` is similar). Output is cut short for space.

```
jon@jons-linux:~$ python3 -q
>>> import forevercal as cal
>>> 
>>> # (01/01/2023) => 'Sunday'
>>> y = cal.PresentableGregorian(2023, day1_weekday='Sunday')
>>> print(y)
            2023
          January
Sun Mon Tue Wed Thu Fri Sat
 1   2   3   4   5   6   7 
 8   9   10  11  12  13  14
 15  16  17  18  19  20  21
 22  23  24  25  26  27  28
 29  30  31                

          February
Sun Mon Tue Wed Thu Fri Sat
             1   2   3   4 
 5   6   7   8   9   10  11
 12  13  14  15  16  17  18
 19  20  21  22  23  24  25
 26  27  28                

             .
             .
             .

          November
Sun Mon Tue Wed Thu Fri Sat
             1   2   3   4 
 5   6   7   8   9   10  11
 12  13  14  15  16  17  18
 19  20  21  22  23  24  25
 26  27  28  29  30        

          December
Sun Mon Tue Wed Thu Fri Sat
                     1   2 
 3   4   5   6   7   8   9 
 10  11  12  13  14  15  16
 17  18  19  20  21  22  23
 24  25  26  27  28  29  30
 31                        


>>> 
```


- `PresentableMonth` interface

```
jon@jons-linux:~$ python3 -q
>>> import forevercal as cal
>>> 
>>> # month=June, year=2023 => common year, (06/01/2023) => 'Thursday'
>>> m = cal.PresentableMonth(6, is_yr_leap=False, day1_weekday='Thursday')
>>> print(m)
          June 
Sun Mon Tue Wed Thu Fri Sat
                 1   2   3 
 4   5   6   7   8   9   10
 11  12  13  14  15  16  17
 18  19  20  21  22  23  24
 25  26  27  28  29  30    


>>> 
>>> 
```

- `PresentableDate` interface

```
jon@jons-linux:~$ python3 -q
>>> import calendar
>>> from datetime import datetime
>>> 
>>> import forevercal as cal
>>> 
>>> #########################################
>>> # create genesis date
>>> #########################################
>>> # python weekdays mapper
>>> wkdays = ['Monday',
...           'Tuesday',
...           'Wednesday',
...           'Thursday',
...           'Friday',
...           'Saturday',
...           'Sunday',]
>>> today = datetime.today()
>>> today
datetime.datetime(2023, 6, 10, 11, 57, 13, 100626)
>>> 
>>> # forevercal genesis date (today)
>>> today = cal.PresentableDate(today.year, today.month, today.day, wkdays[today.weekday()])
>>> print(today)
Saturday, Jun 10 2023
>>> 
>>>
>>> ########################################
>>> # generate other dates from genesis date
>>> ########################################
>>> # 08/20/1972 < today
>>> date = today(1972, 8, 20)
>>> print(date)
Sunday, Aug 20 1972
>>> 
>>> # 02/29/(4 ** 10) > today 
>>> date = today(4 ** 10, 2, 29)
>>> print(date)
Thursday, Feb 29 1048576
>>> 
```
