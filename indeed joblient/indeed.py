from re import X
from turtle import xcor
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd


page_val = 0
jobs_data = []
for i in range(10):
    url = "https://in.indeed.com/jobs?q=software+developer&l=india&sort=date&start={}".format(page_val)
    page_val+=10
    print(url)

    page = requests.get(url)
    print(page)
    #page.text

    driver = webdriver.Chrome("C:\\Users\\aryan19b\\Desktop\\joblient\\indeed joblient\\chromedriver-win64\\chromedriver.exe")
    driver.get(url)

    time.sleep(3)

    soup = BeautifulSoup(driver.page_source,'html.parser')

    #print(soup.prettify())

    driver.close()


    df = pd.DataFrame(columns=['Title','Company','Ratings','Reviews','URL'])

    jobs = soup.findAll(class_='job_seen_beacon')
    #print(jobs[0])

    for job in jobs:
        data = {}
        
        p=job.find('a', class_='jcs-JobTitle css-jspxzf eu4oa1w0')        

        x=job.find('span',class_='companyName')
        if x:
            data['Company']=x.text
    
        if p:
            data['Title'] = p.span.text
    
        x=job.find('span', class_='date')
        if x:
            data['Days Left']=x.text

        x=job.find(class_='companyLocation')
        if x:
            data['Location(s)']=x.text

        if p: 
            data['link'] = p.get('href')
    
        jobs_data.append(data)
    
df = pd.DataFrame(jobs_data)
df.to_csv('indeed_jobs.csv')

