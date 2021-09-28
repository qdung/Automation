from types import ClassMethodDescriptorType
import unittest
from selenium import webdriver
import yaml
import pandas
import time

def getConfig():
  try:
    with open('./config/config.yml') as _file:
      config = yaml.load(_file, Loader=yaml.FullLoader)
      browser = config['browser']
      url = config['url']
      scenarioExcel = config['scenarioExcel']
      loginXpath = config['xpath']
      if (browser == "Chrome"):
        driver = webdriver.Chrome('../drivers/chromedriver.exe')
    return driver, url, scenarioExcel, loginXpath

  except Exception as error:
    print(error)
    return 0

def getLoginCredential(_excelFile):
  dataFrames = pandas.read_excel(_excelFile, "Login")
  usernameList = list(dataFrames['Username'].values)
  passwordList = list(dataFrames['Password'].values)
  return usernameList, passwordList

def login(driver, url, XPath, usernameList, passwordList):
  numberOfUser = len(usernameList)
  for number in range(numberOfUser):
    print(f"user: {usernameList[number]} -- password: {passwordList[number]}")
    driver.get(url)
    driver.implicitly_wait(20)
    # time.sleep(5)
    usernameInput = driver.find_element_by_xpath(XPath['login']['username'])
    driver.implicitly_wait(10)
    usernameInput.send_keys(usernameList[number])
    driver.implicitly_wait(10)
    passwordInput = driver.find_element_by_xpath(XPath['login']['password'])
    driver.implicitly_wait(10)
    passwordInput.send_keys(str(passwordList[number]))
    driver.implicitly_wait(10)
    buttonLogin = driver.find_element_by_xpath(XPath['login']['buttonLogin'])
    driver.implicitly_wait(10)
    buttonLogin.click()
    driver.implicitly_wait(10)
    try:
      acceptButton = driver.find_element_by_xpath(XPath['dashboard']['class'])
      driver.implicitly_wait(5)
      acceptButton.click()
    except Exception as error:
      print(error)
      # print('Next user.........')
    finally:
      print('Next user.........')
      time.sleep(2)
      driver.delete_all_cookies()

def main():
  ( driver, url, scenarioExcel, loginXpath ) = getConfig()
  ( usernameList, passwordList ) = getLoginCredential(scenarioExcel)
  login ( driver, url, loginXpath, usernameList, passwordList )

main()
