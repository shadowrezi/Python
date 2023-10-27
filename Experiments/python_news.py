import requests
from bs4 import BeautifulSoup as bs

r = requests.get('https://www.python.org/blogs/')
soup = bs(r.text, 'lxml')

events = [i.find('a').text for i in soup.find_all('h3', class_='event-title')]

print(events)
