import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import json

url = "https://in.jooble.org/SearchResult?rgns=india&ukw=software%20developer"
params = {
    'txtKeywords': 'developer',
    'txtLocation': 'India'
}

res = requests.get(url)
print(res)
soup = BeautifulSoup(res.text, 'lxml')
soup.title

jobs = soup.find_all('article', class_='ojoFrF rHG1ci')
print(f"Total jobs: {len(jobs)}")

jobs_data = []

for job in jobs:
    data = {}
    
    t=job.section
    x=t.find(class_='heru4z')
    data['Company']=x.p.get_text(strip=False)
        
    data['Title'] = job.header.h2.a.get_text(strip=False)
    
    
    
    data['Days Left'] = t.find(class_='Vk-5Da').get_text(strip=False)

    data['Location(s)']=t.find(class_='caption NTRJBV').get_text(strip=False)

    data['link'] = job.header.h2.a['href']
    
    jobs_data.append(data)
    
df = pd.DataFrame(jobs_data)
df.to_csv('jooble_jobs.csv')

