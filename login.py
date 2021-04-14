from bs4 import BeautifulSoup as bs
import json
from requests import Session

AO3_URL = 'https://archiveofourown.org/'


def get_creds(cred_file):
    with open(cred_file) as f:
        creds = json.load(f)
    return creds

def login(cred_file):
    session = Session()

    site = session.get(AO3_URL)
    bs_content = bs(site.content, 'html.parser')
    auth_token = bs_content.find('meta', {'name':'csrf-token'})['content']

    credentials = get_creds(cred_file)

    login_data = {
        'user[login]': credentials['username'],
        'user[password]': credentials['password'],
        'authenticity_token': auth_token,
    }

    session.post(
        AO3_URL + 'users/login',
        data=login_data,
    )

    return session
