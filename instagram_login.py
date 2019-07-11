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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

username = "scrapeme2019"
password = "ilovescraping"

login_url = "https://www.instagram.com/accounts/login/"
url = "https://www.instagram.com/"
# start chrome browser
driver = webdriver.Chrome('./lib/chromedriver')
LOGGED = False

def load(length=5):
    for i in range(0,length):
        print('. ', end =" ")
        time.sleep(1)
    print("")
    
    
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
        total_following = int(following_button.text[:-10])
        following_button.click()
        load(3)
        # Load all followers (scroll down div item)
        loaded_following = driver.find_elements_by_xpath("//a[@class='FPmhX notranslate _0imsa ']")
        loaded_till_now = len(loaded_following)
        
        while(loaded_till_now<total_following):
            print("following users loaded till now: " + str(loaded_till_now) + " / " + str(total_following))
            loaded_following[loaded_till_now-1].location_once_scrolled_into_view
            driver.find_element_by_tag_name('body').send_keys(Keys.END) # triggers AJAX request to load more users. observed that loading 10 users at a time.
            load(1) 
            loaded_following = driver.find_elements_by_xpath("//a[@class='FPmhX notranslate _0imsa ']")
            loaded_till_now = len(loaded_following)
        print("following users loaded till now: " + str(total_following) + " / " + str(total_following))
        out = [follow.text for follow in loaded_following]
    except NoSuchElementException:
        out =[]
    return out


def get_users_followers(user, second=False):
    if not LOGGED:
        login()
    driver.get(url+user+'/')
    load(3)
    try:
        #click the followers button
        followers_button = driver.find_element_by_xpath('//a[@href="/'+user+'/followers/"]')
        total_following = int(followers_button.text[:-10])
        followers_button.click()
        load(3)
        # Load all followers (scroll down div item)
        loaded_following = driver.find_elements_by_xpath("//a[@class='FPmhX notranslate _0imsa ']")
        loaded_till_now = len(loaded_following)
        
        while(loaded_till_now<total_following):
            print("following users loaded till now: " + str(loaded_till_now) + " / " + str(total_following))
            loaded_following[loaded_till_now-1].location_once_scrolled_into_view
            driver.find_element_by_tag_name('body').send_keys(Keys.END) # triggers AJAX request to load more users. observed that loading 10 users at a time.
            load(1) 
            loaded_following = driver.find_elements_by_xpath("//a[@class='FPmhX notranslate _0imsa ']")
            loaded_till_now = len(loaded_following)
        print("following users loaded till now: " + str(total_following) + " / " + str(total_following))
        second_following = []
        followers = [follow.text for follow in loaded_following]
        
        for follower in followers:
            print(follower)
            if second:
                second_following.extend(get_users_following(follower))
                load(2)
            else:
                second_following.append(follower)
        return second_following
    except NoSuchElementException:
        return []


def get_users_followed_hashtags(users):
    if not LOGGED:
        login()
    followers = []
    for user in users:
        driver.get(url+user+'/')
        load(3)
        try:
            followers_button = driver.find_element_by_xpath('//a[@href="/'+user+'/followers/"]')
            followers_button.click()
            load(3)
            #click on hashtags
            hastags_button = driver.find_element_by_xpath('//button[@class="_0mzm- sqdOP yWX7d    _8A5w5  "]')
            hastags_button.click()
            load(2)
            loaded_following = driver.find_elements_by_xpath("//a[@class='hI7cq']")
            followers.extend([follow.text for follow in loaded_following])
        except NoSuchElementException:
            pass
    return followers
        

def get_top_users(list_users, num_of_users = 20):
    user_class = {}
    for u in list_users:
        if list_users.count(u) > 1:
            user_class[u] = list_users.count(u)
    user_class_sorted = dict(sorted(user_class.items(), key=operator.itemgetter(1), reverse=True))
    return user_class_sorted


def get_top_followed_tags(list_tags, num_of_tags = 20):
    tag_class = {}
    for t in list_tags:
        if list_tags.count(t) > 1:
            tag_class[t] = list_tags.count(t)
    tag_class_sorted = dict(sorted(tag_class.items(), key=operator.itemgetter(1), reverse=True))
    return tag_class_sorted
            
LOGGED = login()
if LOGGED: 
    followers = get_users_followers('transatlanticcrochet')
    top_followers = get_top_users(followers)
    tags = get_users_followed_hashtags(followers)
    top_followers_tags = get_top_followed_tags(tags)
    print("-------------------TOP FOLLOWED------------")
    f= open("top_followed.txt","w+")
    f.write(top_followers)
    f.close()
    print(top_followers)
    print("-------------------TOP TAGS------------")
    f= open("top_followed_tags.txt","w+")
    f.write(top_followers_tags)
    f.close()
    print(top_followers_tags)
    print("all done")

driver.quit();
