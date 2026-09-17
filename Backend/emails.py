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
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://mail.google.com/"
]
flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret.json",
    scopes = SCOPES
)

creds = flow.run_local_server()
print("working")

"""access_token = creds.token
refresh_token = creds.refresh_token
if creds.id_token:
    email = creds.id_token.get("email")
    print("User email:", email)
else:
    print("No email found in the ID token.")

import base64
def xoauth2_string(email, access_token):
    auth_string = f"user={email}\01auth=Bearer {access_token}\x01\x01"
    return base64.b64encode(auth_string.encode()).decode()

def gmail_imap_login(email, access_token):
    xoauth2 = xoauth2_string(email, access_token)
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.authenticate("XOAUTH2", lambda x: xoauth2)
    return imap

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

text = soup.get_text()

imap = gmail_imap_login(email, access_token)
imap.select("INBOX")
status, data = imap.search(None, "ALL")
msgs_ids = data[0].split()
email_pattern = r"|".join(map(re.escape, keyphrases.keys()))
regex = re.compile(email_pattern, re.IGNORECASE)

for eid in msgs_ids:
    status, msg_data = imap.fetch(eid, "(RFC822)")
    raw_email = msg_data[0][1]
    
    msg = email.message_from_bytes(raw_email)
    matches = re.findall(email_pattern, msg.get_payload(decode=True).decode(errors="ignore"))
    

df = pd.DataFrame(matches, columns=["Emails"])
df = df.drop_duplicates()
print(df)"""



 