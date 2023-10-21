import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import json

url = "https://www.timesjobs.com/candidate/job-search.html"
params = {
    'searchType': 'personalizedSearch',
    'from': 'submit',
    'txtKeywords': 'developer',
    'txtLocation': 'India'
}

res = requests.get(url, params=params)
print(res)
soup = BeautifulSoup(res.text, 'lxml')
soup.title

jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
print(f"Total jobs: {len(jobs)}")

jobs_data = []

for job in jobs:
    data = {}

    data['Company'] = job.find('h3', class_='joblist-comp-name').get_text(strip=True)
    
    data['Title'] = job.find('strong', class_='blkclor').get_text(strip=False)
    
    data['Days Left'] = job.find('span', class_='sim-posted').span.get_text(strip=False)

    ul = job.find('ul', class_='top-jd-dtl clearfix').findChildren(recursive=False)
    data['Location(s)'] = ul[1].span.text if ul[1].span else None

    data['link'] = job.header.h2.a['href']
    
    jobs_data.append(data)
    
df = pd.DataFrame(jobs_data)
df.to_csv('times_jobs.csv')

