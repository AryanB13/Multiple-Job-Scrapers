from re import X
from turtle import xcor
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd


page_val = 10
jobs_data = []
for i in range(page_val):
    if i==0:
        continue
    print(i)
    url = "https://www.naukri.com/software-developer-jobs-in-india-{}".format(i)
    url=url+"?jobAge=30"
    print(url)

    page = requests.get(url)
    #page.text

    driver = webdriver.Chrome("C:\\Users\\aryan19b\\Desktop\\testing\\naukri joblient\\chromedriver-win64\\chromedriver.exe")
    driver.get(url)

    time.sleep(3)

    soup = BeautifulSoup(driver.page_source,'html.parser')

    #print(soup.prettify())

    driver.close()


    df = pd.DataFrame(columns=['Title','Company','Ratings','Reviews','URL'])

    jobs = soup.findAll(class_='cust-job-tuple layout-wrapper lay-2 sjw__tuple')
    #print(jobs)

    for job in jobs:
        data = {}
        
        x=job.find('a', class_='comp-name')
        if x:
            data['Company']=x.text
    
        x=job.find('a', class_='title')
        if x:
            data['Title'] = x.text
    
        x=job.find('span', class_='job-post-day')
        if x:
            data['Days Left']=x.text

        x=job.find('span', class_='locWdth')
        if x:
            data['Location(s)']=x.text

        x=job.find('a', class_='title')
        if x: 
            data['link'] = x.get('href')
    
        jobs_data.append(data)
    
df = pd.DataFrame(jobs_data)
df.to_csv('naukri_jobs.csv')

