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
#import instagram_agents
def get_instagram_tags(tag, redlist=[], blocked_words=[], num_of_tags=30):
    tag = str(tag).replace(' ','').split(',')
    log = open("instagram_tags.log","w")
    log.write("INSTAGRAM TAGS: " + str(dt.now())[0:-7] + "\n")
    
    tag_class = {}
    
    def get_caption(html):
        return re.findall(r'{"text":(.*?)}', html)
    
    def get_hashtag_dict(caption, redlist = [], blocked_words = []):
        tags = []
        for txt in caption:
            # Isolate the hashtags from the photo captions
            tmp = re.findall(r'#(.*?) ',txt)
            for t in tmp:
                blocked = []
                # Remove unwanted tags
                for bw in blocked_words:
                    if bw in t:
                        blocked.append(t)
                        log.write(str(dt.now())[0:-7] +": " + bw + " found in " + t + ", ")
                if "\\u" in t or "#" in t  or len(t) > 40 or t in redlist or t in blocked:
                    tmp.remove(t)
                    log.write(str(dt.now())[0:-7] + ": " + t + " was removed\n")
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
        #print(tag_class)
        
    def is_out_of_date(file):
        file_mod_time = os.stat(file).st_mtime
        return (time.time() - file_mod_time) > (30*60)
    
    
    if len(tag) < 1:
        print("No tags input!")
        raise Exception("No tags")
    
    # Clean the tags (in case of user input)
    for i in range(0,len(tag)-1):
        tag[i] = tag[i].lower()
        tag[i] = tag[i].replace(" ","")
    if len(tag)>30:
        tag = tag[0:29]
    """   
    # The tags you want to look up
    tag = ["cheese"]    
    # Add re listed words here
    redlist = ["artesanato","hechoamano", "ganchillo", "feitoamano", \
               "fauxlocs", "tapet3decroche", "croche", "moda", "ulzzang"]
    blocked_words = ["knit", "lik", "follow", "hair", "hecho", "ah", \
                     "hijab", "nak","nik", "baya", "ak", "ja", "lularoe","ulzzang","order"]
    """
    # Number of tags desired
    num_of_tags = 90
    link = []
    for t in tag:
        for i in range(1,11):
            link.append("https://www.instagram.com/explore/tags/"+t+"/?hl=en&?page="+str(i))
            
    if not os.path.exists("data_files"):
        os.makedirs("data_files")
    
    # MAIN   
    for l in link:
        for t in tag:
            html = None
            if os.path.exists("data_files/" + str(t) + ".txt") and os.path.getsize("data_files/" + str(t) + ".txt") > 0:        
                if is_out_of_date("data_files/" + str(t) + ".txt"):
                    #write to file
                    html = urlopen(l).read()
                    html = str(html)
                    html_file = open("data_files/" + str(t) + ".txt","w")
                    html_file.write(html)
                    log.write(str(dt.now())[0:-7] + ": " + "Tag file updated: " + "data_files/" + str(t) + ".txt\n")
                else:
                    html_file = open("data_files/" + str(t) + ".txt","r")
                    html = html_file.read()
                    log.write(str(dt.now())[0:-7] + ": " + "Tag file read from: " + "data_files/" + str(t) + ".txt\n")
            else:
                html = urlopen(l).read()
                html = str(html)
                html_file = open("data_files/" + str(t) + ".txt","w")
                html_file.write(html)
                log.write(str(dt.now())[0:-7] + ": " + "New tag file created: " + "data_files/" + str(t) + ".txt\n")
                
            html_file.close()
            tags = get_hashtag_dict(get_caption(html), redlist, blocked_words)
    # Sort the top amount of tags
    tag_class_sorted = dict(sorted(tag_class.items(), key=operator.itemgetter(1), reverse=True)[:num_of_tags])
    out = ".\n.\n.\n.\n.\n.\n.\n.\n.\n.\n"
    for k in tag_class_sorted.keys():
        out = out + "#" + k + " "
    print(out)
    log.close()
    return {"hashtags":out}
