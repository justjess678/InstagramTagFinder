#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 17:23:59 2019

@author: jessica
"""


import smtplib, re

def sendEmail(destaddr, msg):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", destaddr):
        raise Exception('invalid_email')
    pw = "#tags4all"
    sender = "Tag Finder"
    sender_email = "tagfinderforinsta@gmail.com"
    receiver = destaddr.split('@')[0]
    message = "From: "+sender+" <"+sender_email+">"
    message += "To: "+receiver+" <"+destaddr+">"
    message += """MIME-Version: 1.0
    Content-type: text/html
    Subject: Your Instagram tags are ready!

    <h1>Your hashtags have finished brewing!</h1>
    <p>
    """
    message += """</p><br>
    <h3>If you like this app, <a href="paypal.me/JessChambers27">
    consider making a donation!</a></h3>
    """
    try:
       server = smtplib.SMTP('smtp.gmail.com', 587)
       server.ehlo()
       server.starttls()
       server.sendmail(sender, destadr, message)         
       print("Successfully sent email")
    except SMTPException:
       print("Error: unable to send email")