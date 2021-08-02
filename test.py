from requests_html import HTMLSession
from bs4 import BeautifulSoup

# create an HTML Session object
session = HTMLSession()

# Use the object above to connect to needed webpage
resp = session.get("https://couponscorpion.com/it-software/python-and-flask-demonstrations-practice-course")

# Run JavaScript code on webpage
resp.html.render(sleep=1, keep_page=True, scrolldown=7)

soup = BeautifulSoup(resp.html.html, "html.parser")
a_tag = soup.find("a", class_="btn_offer_block")
print(a_tag.get("href"))