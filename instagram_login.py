#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 12:30:50 2019

@author: jessica
"""

"""
USERNAME

<input class="_2hvTZ pexuQ zyHYP" id="f39a64949f25364" aria-label="Phone number, username, or email"
aria-required="true" autocapitalize="off" autocorrect="off" maxlength="75" name="username" type="text" value="">

PASSWORD

<input class="_2hvTZ pexuQ zyHYP" id="f128f860ba504e8" aria-label="Password" aria-required="true"
autocapitalize="off" autocorrect="off" name="password" type="password" value="">

TOKEN

"csrf_token":"BBET9xjbj6rTnAKjipKUQg8BAZUw8Ycz"

"""
import time
from selenium import webdriver

username = "scrapeme2019"
password = "ilovescraping"

login_url = "https://www.instagram.com/accounts/login/"
url = "https://www.instagram.com/"
# start chrome browser
driver = webdriver.Chrome('./lib/chromedriver')

def login():
    # prepare the option for the chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    
    driver.get(login_url)
    dom = driver.find_element_by_xpath('//*')
    
    #pdb.set_trace()
    username_in = dom.find_element_by_name("username")
    password_in = dom.find_element_by_name("password")
    login_button = dom.find_element_by_xpath('//*[@type="submit"]')
    
    username_in.clear()
    password_in.clear()
    username_in.send_keys(username)
    password_in.send_keys(password)
    
    login_button.click()
    for i in range(0,5):
        print(5-i,'\n...\n')
        time.sleep(1)
    
    if 'logged-in' in driver.page_source:
        print('Logged in successfully')
        return True
    else:
        return False

def get_users_followers(user):
    if login():
        driver.get(url+user+'/followers/')
    #class=wo9IH
    #all_followers = driver.find_elements_by_xpath("//*[@class='wo9IH']")
    #for follower in all_followers:
        #print(follower.text)
    
get_users_followers('jesscomix')
print("all done")

#driver.quit();
