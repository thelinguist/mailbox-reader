import glob
import emlx
import os
from identify_company import identify_company
from typing import TypedDict

mailbox_path = os.path.expanduser("~/") + "Library/Mail/**/*.emlx"

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

def read_mailbox(source_email: str, index: int):
    companies = []
    for filepath in glob.iglob(mailbox_path, recursive=True):
        index += 1
        m = emlx.read(filepath)
        to = m.headers.get("To") or m.headers.get("Delivered-To")
        if to:
            if source_email in to:
                subject = m.headers.get("Subject")
                if subject:
                    company = identify_company(subject.lower())
                    if company:
                        date = m.headers.get("Date")
                        companies.append((company, date))
        if index % 100 == 0:
            print("processed ", index, "emails")
    return companies

