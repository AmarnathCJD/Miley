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

typex = "chrome"
  
@register(pattern="^/edutest ?(.*)")
async def edu(event):
 await gen_edu(event)
  
  
async def gen_edu(event):
 try:
  studentPhone = random_phone_num_generator()
  ex_split = studentAddress.split("\n")
  streetAddress = ex_split[0]
  if(re.compile(',').search(ex_split[1]) != None):
        ex_split1 = ex_split[1].split(', ')
        cityAddress = ex_split1[0]
        ex_split2 = ex_split1[1].split(' ')
        stateAddress = ex_split2[0]
        postalCode = ex_split2[1]
  else:
        ex_split3 = ex_split[1].split(' ')
        cityAddress = ex_split3[0]
        stateAddress = ex_split3[1]
        postalCode = ex_split3[2]
  random.seed()
  letters = string.ascii_uppercase
  middleName = random.choice(letters)
  chrome_options = webdriver.ChromeOptions()
  try:
    driver = webdriver.Chrome(chrome_options=chrome_options)
  except Exception as e:
   return await event.reply(f"{e}")
  driver.maximize_window()
  driver.get(start_url)
  WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "accountFormSubmit"))
    ).click()
  x = await event.reply("Account Progress - 1/3")
  WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "inputFirstName"))
    ).send_keys(firstName)

  time.sleep(0.7)
  WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "inputMiddleName"))
    ).send_keys(middleName)
  time.sleep(0.7)
  WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "inputLastName"))
    ).send_keys(LastName)
  time.sleep(0.7)
  driver.find_element_by_xpath('//*[@id="hasOtherNameNo"]').click()
  driver.find_element_by_xpath('//*[@id="hasPreferredNameNo"]').click()
  time.sleep(0.7)
  WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#inputBirthDateMonth option[value="' + str(randomMonth) + '"]'))
    ).click()
  time.sleep(0.7)
  await x.edit("success upto now")
 except Exception as e:
    print(e)
