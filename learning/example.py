# This file will read messages in my Apple Mail inbox and print the first 5, their subjects, senders, and a few lines from the content.

import emlx
import glob
import os
import sys

From = tuple['From', str]
To = tuple['To', str]
ReplyTo = tuple['Reply-To', str]
Date = tuple['Date', str]
Subject = tuple['Subject', str]
Received = tuple['Received', str]
ReturnPath = tuple['Return-Path', str]
DeliveredTo = tuple['Delivered-To', str]
DeliveryDate = tuple['Delivery-date', str]
MessageId = tuple['Message-Id', str]
SpamHeaders = tuple['X-Proofpoint-Spam-Details', str]

# otherHeaders = ['X-Proofpoint-GUID', 'X-Proofpoint-Virus-Version', 'Content-Type', 'MIME-Type', 'Envelope-to', 'DKIM-Signature']

Headers = dict[ReturnPath, DeliveredTo, DeliveryDate, From, To, ReplyTo, Date, Subject, Received, MessageId, SpamHeaders]





mailbox_path = os.path.expanduser("~/") + "Library/Mail/**/*.emlx"
print(mailbox_path)

example = "/Users/bryce/Library/Mail/V10/71B37316-531B-4A3F-8B6E-527A6C5DDF00/INBOX.mbox/13DB188E-3D10-4AB5-95C8-30C7FBE360C6/Data/4/3/4/Messages/434222.emlx"
m = emlx.read(example)
print(m.headers['From'], m.headers['To'], m.headers['Date'], m.headers['Subject'])
print(m.text)
print(m.plist)
