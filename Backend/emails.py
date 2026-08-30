import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

url = "https://www.w3.org/Consortium/contact"  
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

text = soup.get_text()

email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
emails = re.findall(email_pattern, text)

df = pd.DataFrame(emails, columns=["Email"])
df = df.drop_duplicates()
print(df)



 