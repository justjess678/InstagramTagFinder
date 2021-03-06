#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 15:38:24 2019

@author: jessica
"""
import time
import instagram_tags as insta
from tkinter import *

fields = 'Tags', 'Banned tags', 'Banned words', 'Number of tags'

def fetch(entries):
   for entry in entries:
      field = entry[0]
      text  = entry[1].get()
      print('%s: "%s"' % (field, text)) 

def makeform(root, fields):
   entries = []
   num = 0
   for field in fields:
      num += 1
      row = Frame(root)
      lab = Label(row, width=15, text=field, anchor='w')
      if field != 'Number of tags':
          ent = Entry(row)
      else:
          ent = Spinbox(row, from_=0, to=60, value=30)
      row.grid(column=0,columnspan=2,padx=5, pady=5,row=num)
      lab.grid(column=0,columnspan=1,padx=5, pady=5,row=num)
      ent.grid(column=1,columnspan=1,row=num)
      entries.append((field, ent))
   return entries, num

tag_info = {}
var = None
result_text=None

def get_tags(tag, redlist, blocked_words, num_of_tags = 30):
    tag_info = insta.get_instagram_tags(tag, redlist, blocked_words, num_of_tags)
    var.set('')
    var.set(str(tag_info.get('hashtags','')))
    result_text.delete('1.0', END)
    result_text.insert('1.0', var.get())

def clear(ents):
    for e in ents:
        if e != ents[3]:
            e[1].delete(0, 'end')

if __name__ == '__main__':
   root = Tk()
   root.title("Instagram Tag Generator")
   var = StringVar(root)
   
   ents, num = makeform(root, fields)
   root.bind('<Return>', (lambda event, e=ents: get_tags(e[0][1].get(),e[1][1].get(),e[2][1].get(), e[3][1].get())))
   
   info_label = Label(root, text='Input tags separated by commas\neg: "cat, dog".\n\nBlocked tags are entire\ntags that will not be shown.\n\nIf a tag contains a blocked\nword it will not be shown')
   info_label.grid(column=2, columnspan=2,row=1,rowspan=3, padx=5, pady=5)
   
   clear_button = Button(root, text='Clear',
          command=lambda: clear(ents))
   clear_button.grid(column=0,columnspan=1, padx=5, pady=5, row=num+1)
   
   show_button = Button(root, text='Show',
          command=lambda: get_tags(ents[0][1].get(),ents[1][1].get(),ents[2][1].get(), ents[3][1].get()))
   show_button.grid(column=2,columnspan=1, padx=5, pady=5, row=num+1)
   
   result_text = Text(root)
   result_text.grid(column=0,columnspan=3, padx=5, pady=5, row=num+2, rowspan=3)
   result_text.insert('1.0',tag_info.get('hashtags',''))
   
   root.mainloop()
   
