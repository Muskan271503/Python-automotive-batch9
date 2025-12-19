#child module
import builtin
print(builtin(5))

from math import sqrt, factorial
print(sqrt(16))
print(factorial(16))

#builtin module --> math, random, datetime, os, sys, json, re, statistics, itertools, functools, collections
import random
print(random.randint(1, 5))  # prints a random integer between 1 and 5

#user define module --> calc.py , builtin.py
#3rd party module --> numpy, pandas, matplotlib, requests, flask, django

import requests
response = requests.get("https://google.com")
response.status_code  # prints the status code of the response

