#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 20:59:00 2019

@author: Jessica Chambers
"""
from urllib.request import urlopen
import re
import operator
# The tag you want to look up
tag = ["crochet","fashion"]
# Add re listed words here
redlist = ["artesanato","hechoamano", "ganchillo", "knitting", "feitoamano", \
           "fauxlocs", "tapetedecroche", "knit", "croche", "moda"]
# Number of tags desired
num_of_tags = 30
link = []
for t in tag:
 link.append("https://www.instagram.com/explore/tags/"+t+"/?hl=en")

for i in range(0,10):
    for l in link:
        html = urlopen(l).read()
        html = str(html)
        m = re.findall(r'{"text":(.*?)}', html)
        tag_class = {}
        for txt in m:
            tmp = re.findall(r'#(.*?) ',txt)
            for t in tmp:
                if "\\" in t or "#" in t or t in tag or len(t) > 40 or t in redlist:
                    tmp.remove(t)
                else:
                    if t in tag_class:
                        tag_class[t] = tag_class.get(t) + 1
                    else:
                        tag_class[t] = 1

tag_class_sorted = dict(sorted(tag_class.items(), key=operator.itemgetter(1), reverse=True)[:num_of_tags])
print(tag_class_sorted)
