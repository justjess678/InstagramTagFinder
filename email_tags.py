#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 17:23:59 2019

@author: jessica
"""


import smtplib

def sendEmail(destaddr, msg):
    sender = ""
    sender_email = ""
    message = "From: From Person <from@fromdomain.com>"
    message += "To: To Person <"+destaddr+">"
    message += """MIME-Version: 1.0
    Content-type: text/html
    Subject: Your Instagram tags are ready!

    <h1>Your hashtags have finsihed brewing!</h1>
    <p>
    """
    
    try:
       smtpObj = smtplib.SMTP('localhost')
       smtpObj.sendmail(sender, receivers, message)         
       print("Successfully sent email")
    except SMTPException:
       print("Error: unable to send email")