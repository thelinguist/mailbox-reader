from dotenv import load_dotenv
import emlx
import glob
import os
from pandas import DataFrame as df

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

##### TYPINGS #####
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

Headers = dict[
    ReturnPath, DeliveredTo, DeliveryDate, From, To, ReplyTo, Date, Subject, Received, MessageId, SpamHeaders]


def get_company(subject: str):
    for slug in APPLICATION_SUBJECT_SLUGS_PREFIX:
        if slug in subject:
            company = subject.split(slug)[0]
            # remove punctuation
            company = not company[-1].isalnum() and company[:-1] or company
            # trim whitespace
            return company.strip()

    for slug in APPLICATION_SUBJECT_SLUGS:
        if slug in subject:
            company = subject.split(slug)[1]
            # remove punctuation
            company = not company[-1].isalnum() and company[:-1] or company
            # trim whitespace
            return company.strip()
    return None


def read_mailbox(index: int):
    companies = []

    for filepath in glob.iglob(mailbox_path, recursive=True):
        index += 1

        m = emlx.read(filepath)
        to = m.headers.get("To") or m.headers.get("Delivered-To")
        if to:
            if EMAIL_ADDRESS in to:
                subject = m.headers.get("Subject")
                if subject:
                    company = get_company(subject.lower())

                    if company:
                        date = m.headers.get("Date")
                        companies.append((company, date))

        if index % 100 == 0:
            print("processed ", index, "emails")
    return companies


applications = read_mailbox(start_at)
for application in applications:
    print("applied to", application[0], " on", application[1])

# write to csv
df(applications, columns=["Company", "Date"]).to_csv("applications.csv", index=False)
