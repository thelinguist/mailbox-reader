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

def identify_company(subject: str):
    """
    This function simply identifies company names based on expected phrasing, either before or after the company name
    :param subject:
    :return:
    """
    for slug in APPLICATION_SUBJECT_SLUGS_PREFIX:
        if slug in subject:
            # to unpack the first item of an array, you must declare the next item with *nextItem(s)
            company, *_ = subject.split(slug)
            company = not company[-1].isalnum() and company[:-1] or company
            return company.strip()
    for slug in APPLICATION_SUBJECT_SLUGS:
        if slug in subject:
            company = subject.split(slug)[1]
            company = not company[-1].isalnum() and company[:-1] or company
            return company.strip()
    return None
