from dotenv import load_dotenv
import os
from pandas import DataFrame as df
from mailbox_reader import read_mailbox
from typing import TypedDict, Optional

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
if not EMAIL_ADDRESS:
    print("Please set EMAIL_ADDRESS in .env file")
    exit()
mailbox_path = os.path.expanduser("~/") + "Library/Mail/**/*.emlx"
start_at = 0

APPLICATION_SUBJECT_SLUGS = [
    "thank you for applying to ",
    "thank you for your application to ",
    "you've been referred to a career opportunity at ",
    "your application with ",
    "thank you for your interest in ",
    "application follow up from ",
]
APPLICATION_SUBJECT_SLUGS_PREFIX = [
    " viewed your application",
]

class Headers(TypedDict, total=False):
    ReturnPath: str
    DeliveredTo: str
    DeliveryDate: str
    From: str
    To: str
    ReplyTo: str
    Date: str
    Subject: str
    Received: str
    MessageId: str
    SpamHeaders: str

applications = read_mailbox(EMAIL_ADDRESS, start_at)
for application in applications:
    print("applied to", application[0], " on", application[1])

# write to csv
df(applications, columns=["Company", "Date"]).to_csv("../applications.csv", index=False)
