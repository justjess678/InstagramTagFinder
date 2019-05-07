#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 20:59:00 2019

@author: Jessica Chambers
"""
from urllib.request import urlopen, HTTPError
import re
import operator
import os
import time
from datetime import datetime as dt

log = open("instagram_tags.log","w")
log.write("INSTAGRAM TAGS: " + str(dt.now())[0:-7] + "\n")

tag_class = {}
num_photos = 0
out = ".\n.\n.\n.\n.\n.\n.\n.\n.\n.\n"
percentages = ""
tag_tuples = []
tag_class_sorted = {}
list_tags = []
data_files_path = "data_files/"

def get_caption(html):
    return re.findall(r'{"text":(.*?)}', html)

def get_hashtag_dict(caption, redlist = [], blocked_words = []):
    tags = []
    for txt in caption:
        # Isolate the hashtags from the photo captions
        txt = txt.lower()
        tmp = re.findall(r'#(.*?) ',txt)
        for t in tmp:
            blocked = []
            # Remove unwanted tags
            for bw in blocked_words:
                if bw in t:
                    blocked.append(t)
                    #log.write(str(dt.now())[0:-7] +": " + bw + " found in " + t + ", ")
            if "\\u" in t or "#" in t or len(t) > 40 or t in redlist or t in blocked:
                tmp.remove(t)
                #log.write(str(dt.now())[0:-7] + ": " + t + " was removed\n")
            else:
                if t not in tags:
                    tags.append(t)
                # Count the occurances of the hashtags
                if t in tag_class:
                    tag_class[t] = tag_class.get(t) + 1
                else:
                    tag_class[t] = 1
    if tag_class == {}:
        raise Exception("No associated hashtags!")
    return tags
    
def is_out_of_date(file):
    return (time.time() - os.stat(file).st_mtime) > (30*60)

# The tags you want to look up
tag = ["mountain"]

if len(tag) < 1:
    raise Exception("No tags")

# Clean the tags (in case of user input)
for i in range(0,len(tag)-1):
    tag[i] = tag[i].lower().replace(" ","")
    
if len(tag)>30:
    tag = tag[0:29]
    
# Add re listed words here
redlist = ["artesanato","hechoamano", "ganchillo", "feitoamano", \
           "fauxlocs", "tapetedecroche", "croche", "moda"]
blocked_words = ["knit", "cake", "choc", "like", "follow"]

if not os.path.exists("data_files"):
    os.makedirs("data_files")
    
# Number of tags desired
num_of_tags = 30
html = None
html_string = ""
err=False

for t in tag:
    if os.path.exists(data_files_path + t + ".txt") and os.path.getsize(data_files_path + t + ".txt") > 0 \
    and not is_out_of_date(data_files_path + t + ".txt"):
        try:
            data_file = open(data_files_path + t + ".txt","r")
            html = data_file.read()
            data_file.close()
        except Exception as e:
                print(e)
                err=True
    else:
        for i in range(1,11):
            l = ("https://www.instagram.com/explore/tags/"+t+"/?hl=en&?page="+str(i))
            try:
                html = urlopen(l).read()
                data_file = open(data_files_path + t + ".txt","w+")
                data_file.write(str(html))
                data_file.close()
            except Exception as e:
                print(e)
                err=True
    #trim unecessary HTML
    head, sep, tail = str(html).partition('</svg></span>')
    head, sep, tail = tail.partition('</script>\n<script type="text/javascript">window.__initialDataLoaded(window._sharedData);</script>')
    html_string += head
    list_tags=(get_hashtag_dict(get_caption(html_string), redlist, blocked_words))

num_photos = html_string.count("src")
        
# Sort the top amount of tags
tag_class_sorted = dict(sorted(tag_class.items(), key=operator.itemgetter(1), reverse=True)[:num_of_tags])

for k in tag_class_sorted.keys():
    tag_tuples.append((tag_class_sorted.get(k), k))
tag_tuples.sort(key=lambda tup: -tup[0])
for tt in tag_tuples:
    out += "#" + tt[1] + " "
    percentages += tt[1] + " = " + str(round(tt[0]/num_photos*100)) + "% of photos\n"
print(out)
print("\n\n\n\n")
print(percentages)
log.close()
result = {"hashtags":out, "stats":percentages, "err":err}
