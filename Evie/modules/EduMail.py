import time
import re
import string
from faker import Faker
import random
import sys
import colorama
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from random import randint

from Evie import tbot, CMD_HELP
from Evie.events import register
from Evie.function import is_admin

"""Variables"""
start_url = 'https://www.opencccapply.net/gateway/apply?cccMisCode='

clg_ids = ['941', '311', '361', '233']

allColleges = ['MSJC College', 'Contra Costa College', 'City College', 'Sacramento College']

country_codes = ['855', '561', '800', '325', '330', '229']

fake = Faker('en_US')

ex = fake.name().split(' ')

firstName = ex[0]
LastName = ex[1]
studentAddress = fake.address()
randomMonth = random.randint(1, 12)
randomDay = random.randint(1, 27)
randomYear = random.randint(1996, 1999)
randomEduMonth = random.randint(1, 12)
randomEduDay = random.randint(1, 27)
eduYears = [2019, 2020]
randomEduYear = random.choice(eduYears)
"""End"""

def postFix(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def random_phone_num_generator():
    first = str(random.choice(country_codes))
    second = str(random.randint(1, 888)).zfill(3)
    last = (str(random.randint(1, 9998)).zfill(4))
    while last in ['1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888']:
        last = (str(random.randint(1, 9998)).zfill(4))
    return '{}-{}-{}'.format(first, second, last)
  
  @register(pattern="^/edutest ?(.*)")
  asymc def edu(event):
    studentPhone = random_phone_num_generator()
    output = f"""
 {firstName}{LastName}\n{studentAddress}\n{randomYear}/{randomDay}/{randomMonth}\n{studentPhone}
 """
    await event.reply(output)
  
  
  
