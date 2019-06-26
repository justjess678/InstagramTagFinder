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
import operator, time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

username = "scrapeme2019"
password = "ilovescraping"

login_url = "https://www.instagram.com/accounts/login/"
url = "https://www.instagram.com/"
# start chrome browser
driver = webdriver.Chrome('./lib/chromedriver')
LOGGED = False

def load(length=5):
    for i in range(0,length):
        print(length-i,'... ')
        time.sleep(1)

def login():
    
    # prepare the option for the chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    
    driver.get(login_url)
    dom = driver.find_element_by_xpath('//*')
    load(1)
    
    #pdb.set_trace()
    username_in = dom.find_element_by_name("username")
    password_in = dom.find_element_by_name("password")
    login_button = dom.find_element_by_xpath('//*[@type="submit"]')
    
    username_in.clear()
    password_in.clear()
    username_in.send_keys(username)
    password_in.send_keys(password)
    
    login_button.click()
    load()
    
    if 'logged-in' in driver.page_source:
        print('Logged in successfully')
        return True
    else:
        return False

def get_users_following(user):
    if not LOGGED:
        login()
    driver.get(url+user+'/')
    load(3)
    try:
        following_button = driver.find_element_by_xpath('//a[@href="/'+user+'/following/"]')
        following_button.click()
        load(3)
        all_following = driver.find_elements_by_xpath("//a[@class='FPmhX notranslate _0imsa ']")
        out = [follow.text for follow in all_following]
    except NoSuchElementException:
        out =[]
    return out


def get_users_followers(user):
    if not LOGGED:
        login()
    driver.get(url+user+'/')
    load(3)
    try:
        followers_button = driver.find_element_by_xpath('//a[@href="/'+user+'/followers/"]')
        followers_button.click()
        load(3)
        all_followers = driver.find_elements_by_xpath("//a[@class='FPmhX notranslate _0imsa ']")
        second_following = []
        followers = [follow.text for follow in all_followers]
        for follower in followers:
            print(follower)
            second_following.extend(get_users_following(follower))
            load(2)
            print("Next follower:")
    except NoSuchElementException:
        second_following =[]
    return second_following

def get_top_users(list_users, num_of_users = 20):
    user_class = {}
    for u in list_users:
        if u in user_class:
            user_class[u] = user_class.get(u) + 1
        else:
            user_class[u] = 1
    user_class_sorted = dict(sorted(user_class.items(), key=operator.itemgetter(1), reverse=True))
    return user_class_sorted
            
LOGGED = login()
if LOGGED: 
    followers = get_users_followers('jesscomix')
    top = get_top_users(followers)
    print(top)
    print("all done")

driver.quit();
