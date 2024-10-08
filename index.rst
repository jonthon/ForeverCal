====
NAME:
====

``forevercal`` is named after forever calendar. It determines a weekday of any date of any given year.


======
MOTIVE:
======

The main motive of this module is to improve explicitness from the built-in python weekday interface (``calendar.weekday``). 

Python weekday hardcodes its index => weekday mapper: 0 => 'Mon', 1 => 'Tue', 2 => 'Wed', ... etc. Compared to this module, that mapper is True for genesis date 1/1/1. However, this module offers more flexibility to specify a custom genesis date (Yes, even today) with args ``(y, m, d, weekday)`` to ``*Date`` interfaces. A genesis date derives a new mapper that's compatible with a specified subject date (even earlier than the genesis date). However, it only works for any given year > 0.


===========
DESCRIPTION:
===========

This module implements an algorithm for determining the weekday (Sun, Mon, Tue, ... etc) of any date given a known weekday of a prime date (genesis date). The algorithm was developed by the author of this module from scratch and tested locally, see the top level code in this file.

``Presentable*`` classes are the recommended interfaces to use because they are the highest level interfaces, easy to use, and follow a simplicity approach. They are also reusable to various front ends: console, GUI, Web, ... etc. They define ``__str__`` for printing. ``Presentable*`` month and year interfaces define ``__iter__`` which makes them iterable, yielding weeks on demand. Ideal for use in GUI and Web frontends since ``__str__`` may not be suitable.

Source code: https://github.com/jonthon/ForeverCal


========
EXAMPLES:
========

- ``PresentableGregorian`` interface use case (``PresentableJulian`` is similar). Output is cut short for space.

::

jon@jons-linux:~$ python3 -q
>>> from forevercal import PresentableGregorian as Gregorian
>>> from datetime import datetime
>>> class Year(Gregorian):
...     WKDAY1 = 'Monday'   # 'Sunday' is default
... 
>>> this_year = datetime.today().year
>>> this_year = Year(this_year)
>>> print(this_year)
            2024            
          January           
Mon Tue Wed Thu Fri Sat Sun
  1   2   3   4   5   6   7
  8   9  10  11  12  13  14
 15  16  17  18  19  20  21
 22  23  24  25  26  27  28
 29  30  31                

          February          
Mon Tue Wed Thu Fri Sat Sun
              1   2   3   4
  5   6   7   8   9  10  11
 12  13  14  15  16  17  18
 19  20  21  22  23  24  25
 26  27  28  29
          .
          .
          .
          November          
Mon Tue Wed Thu Fri Sat Sun
                  1   2   3
  4   5   6   7   8   9  10
 11  12  13  14  15  16  17
 18  19  20  21  22  23  24
 25  26  27  28  29  30    

          December          
Mon Tue Wed Thu Fri Sat Sun
                          1
  2   3   4   5   6   7   8
  9  10  11  12  13  14  15
 16  17  18  19  20  21  22
 23  24  25  26  27  28  29
 30  31 


- `PresentableMonth` interface use case.

:: 

jon@jons-linux:~$ python3 -q
>>> from forevercal import PresentableMonth as Month
>>> today      = datetime.today()
>>> this_month = Month(today.year, today.month)
>>> print(this_month)
         September          
Sun Mon Tue Wed Thu Fri Sat
  1   2   3   4   5   6   7
  8   9  10  11  12  13  14
 15  16  17  18  19  20  21
 22  23  24  25  26  27  28
 29  30
  

- `PresentableDate` interface use case.

::

jon@jons-linux:~$ python3 -q
>>> from forevercal import PresentableDate as Date, map_weekdays
>>> from datetime import datetime
>>> 
>>> pyWeekdays = map_weekdays('Monday', 0)
>>> today      = datetime.today()
>>> today      = today.year, today.month, today.day, pyWeekdays[today.weekday()]
>>> today      = Date(*today)
>>> sep11      = 2001, 9, 11
>>> today.weekday(*sep11)
'Tuesday'
>>>
 
  
