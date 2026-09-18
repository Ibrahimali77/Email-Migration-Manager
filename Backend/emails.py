import requests
import pandas as pd
import re
import imaplib
import email
from google_auth_oauthlib.flow import InstalledAppFlow
from bs4 import BeautifulSoup

url = "https://www.w3.org/Consortium/contact"  
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

# template example of getting a url, scraping it for html, and then parsing it to extract text

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://mail.google.com/"
]

# scopes for API access, make sure they match or it wont consent

flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret.json",
    scopes = SCOPES
)

# download client secret from gcc and put it in root directory

creds = flow.run_local_server()
access_token = creds.token
refresh_token = creds.refresh_token

user_email = "thereal.ib1515@gmail.com"
# this is a placeholder, fix by fetching email address using google api

import base64
def xoauth2_string(email, access_token):
    return f"user={email}\1auth=Bearer {access_token}\1\1".encode()

# the IMAP module requires an XOAUTH2 authentication string

def gmail_imap_login(email, access_token):
    xoauth2 = xoauth2_string(email, access_token)
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.authenticate("XOAUTH2", lambda x: xoauth2_string(user_email, access_token))
    return imap

#Connects to GMAIL IMAP through SSL, authenticates using previous function and returns the session object

keyphrases = {"verify your email": True,
    "confirm your email": True,
    "confirm your account": True,
    "activate your account": True,
    "welcome to": True,
    "thanks for signing up": True,
    "reset your password": True,
    "password reset": True,
    "login alert": True,
    "security alert": True,
    "order confirmation": True,
    "payment confirmation": True,
    "subscription is active": True}

#Possible keywords which may indicate an account exists for that email


imap = gmail_imap_login(user_email, access_token)
imap.select("INBOX")
status, data = imap.search(None, "ALL")
msgs_ids = data[0].split()[:100]
email_pattern = r"|".join(map(re.escape, keyphrases.keys()))
regex = re.compile(email_pattern, re.IGNORECASE)

# login to IMap, select inbox, search for all email ids
# builds a regex of the dictionary keys as the findall method only takes a regex as a parameter

for eid in msgs_ids:
    status, msg_data = imap.fetch(eid, "(RFC822)")
    raw_email = msg_data[0][1]
    
    msg = email.message_from_bytes(raw_email)
    payload = msg.get_payload(decode=True)
    if payload:
        body = payload.decode(errors = "ignore")
    else:
        body = ""
    matches = re.findall(email_pattern, body)
# loop through all emails, extract the raw email bytes, parse the raw email into an object, 
# extract the body and find all the matches of the pattern in the body of the email
    

df = pd.DataFrame(matches, columns=["Emails"])
df = df.drop_duplicates()
print(df)
# display all data using pandas



 