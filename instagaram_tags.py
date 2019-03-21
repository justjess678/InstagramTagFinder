#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 20:59:00 2019

@author: Jessica Chambers
"""
from urllib.request import urlopen, HTTPError
import re
import operator

tag_class = {}

# The tag you want to look up
tag = ["crochet","fashion"]
# Clean the tags (in case of user input)
for i in range(0,len(tag)):
    tag[i] = tag[i].lower()
    tag[i] = tag[i].replace(" ","")
# Add re listed words here
redlist = ["artesanato","hechoamano", "ganchillo", "knitting", "feitoamano", \
           "fauxlocs", "tapetedecroche", "knit", "croche", "moda"]
# Number of tags desired
num_of_tags = 30
link = []
for t in tag:
    for i in range(1,16):
        link.append("https://www.instagram.com/explore/tags/"+t+"/?hl=en&?page="+str(i))

def get_caption(html):
    return re.findall(r'{"text":(.*?)}', html)

def get_hashtag_dict(tag, redlist, caption):
    for txt in caption:
        # Isolate the hashtags from the photo captions
        tmp = re.findall(r'#(.*?) ',txt)
        for t in tmp:
            # Remove unwanted tags
            if "\\" in t or "#" in t or t in tag or len(t) > 40 or t in redlist:
                tmp.remove(t)
            else:
                # Count the occurances of the hashtags
                if t in tag_class:
                    tag_class[t] = tag_class.get(t) + 1
                else:
                    tag_class[t] = 1
    #print(tag_class)
# MAIN   
for l in link:
    html = urlopen(l).read()
    html = str(html)
    get_hashtag_dict(tag, redlist, get_caption(html))
# Sort the top amount of tags
tag_class_sorted = dict(sorted(tag_class.items(), key=operator.itemgetter(1), reverse=True)[:num_of_tags])
print(tag_class_sorted)
