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
import requests
from lxml import html
import re

username = "scrapeme2019"
password = "ilovescraping"

session_requests = requests.session()

login_url = "https://www.instagram.com/accounts/login/"
url = "https://www.instagram.com/"
result = session_requests.get(login_url)

csrf_token = re.findall(r'{"config":{"csrf_token":"(.*?)","viewer"',result.text)[0]

payload = {"username": username, "password": password, "csrf_token": csrf_token}

result = session_requests.post(
	login_url, 
	data = payload, 
	headers = dict(referer=login_url)
)

 # Scrape url
result = session_requests.get(url, headers = dict(referer = url))
print(result.text)
