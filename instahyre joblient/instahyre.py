from re import X
from turtle import xcor
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

page_val = 10
jobs_data = []
url = "https://www.instahyre.com/search-jobs?company_size=0&isLandingPage=true&job_type=0&location=Bangalore&offset=0&search=true&skills=software"
print(url)

page = requests.get(url)

driver = webdriver.Chrome("C:\\Users\\aryan19b\\Desktop\\testing\\instahyre joblient\\chromedriver-win64\\chromedriver.exe")
driver.get(url)

time.sleep(3)


df = pd.DataFrame(columns=['Title', 'Company', 'Ratings', 'Reviews', 'URL'])

#next_page = driver.find_element(By.XPATH, '//*[@id="job-function-page"]/div[2]/div/div[1]/div[1]/div[21]/li[12]').click()
#time.sleep(3)
for i in range(page_val):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    jobs = soup.findAll(class_='employer-row')
    #print(jobs)
    for job in jobs:
            data = {}
    
            company_post = job.find(class_='company-name').text
            #print(company_post)
            parts = company_post.split("-", 1)
            company = parts[0].strip()
            #print(company)
            post = parts[1].strip()
            #print(post)
            data['Company'] = company
            data['Title'] = post

            x = job.find('span', class_='ng-binding ng-scope')
            if x:
                location = x.text.split("in", 1)[1]
                data['Location(s)'] = location

            x = job.find('a', class_='text-link')
            if x:
                data['link'] = x.get('href')

            jobs_data.append(data)
    next_button = driver.find_element(By.XPATH, '//*[@id="job-function-page"]/div[2]/div/div[1]/div[1]/div[21]/li[12]')
    next_button.click()
    time.sleep(3)   
    
driver.close()

df = pd.DataFrame(jobs_data)
df.to_csv('instahyre_jobs.csv')
