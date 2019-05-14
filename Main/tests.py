import datetime
import os
import re

from django.test import TestCase

startDate = datetime.datetime.strptime('1/8/2017', "%d/%m/%Y")
endDate = datetime.datetime.strptime('1/8/2018', "%d/%m/%Y")


l = ['25/8/2017','1/9/2017','1/11/2017',"27/8/2017","7/8/2018","5/12/2017","4/1/2018","3/2/2018","4/7/2018","2/11/2018","3/4/2018","5/9/2018","7/11/2018"]

lst = []
for i in l:
    sr = datetime.datetime.strptime(i, "%d/%m/%Y")
    if sr > startDate and sr < endDate:
        lst.append(i)
print(lst)