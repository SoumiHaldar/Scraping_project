import time
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
import dateparser
import string
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent

ua = UserAgent()
RandomUserAgent = ua.random
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={RandomUserAgent}')
options.add_argument('ignore-certificate-errors')
options.add_argument('incognito')
options.add_argument("--disable-notifications")
options.add_argument("--start-maximized")
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

startUrl='https://www.youtube.com/@tseries/videos'
driver.get(startUrl)
time.sleep(4)
urls=[]
all_dates=[]

for _ in range(25):
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(2)
try:
    soup=BeautifulSoup(driver.page_source,'html.parser')
    time.sleep(4)
    page_table=soup.find('div',{'id':'contents','class':'style-scope ytd-rich-grid-renderer'}).find_all('div',class_='style-scope ytd-rich-item-renderer')
    for each_song in page_table:
        song_link='https://www.youtube.com'+each_song.find('a')['href']
        driver.get(song_link)
        time.sleep(8)
        page_soup=BeautifulSoup(driver.page_source,'html.parser')
        time.sleep(4)
        details=page_soup.find_all('span',class_='bold style-scope yt-formatted-string')
        posted_date=details[2].text
        posted_date1=dateparser.parse(posted_date).strftime('%d/%m/%Y')
        start_date=datetime(2023,5,22)
        # formatted_start_date=start_date.strftime("%d/%m/%Y")
        end_date=datetime(2023,8,8)
        # formatted_end_date=end_date.strftime("%d/%m/%Y")
        date_format = '%d/%m/%Y'
        posted_date2=datetime.strptime(posted_date1, date_format)
        if start_date <= posted_date2 <= end_date:
            print(song_link)
            urls.append(song_link)
            all_dates.append(posted_date1)
        elif posted_date2 < start_date:
            break
        
    # print(urls)
    # print(all_dates)
    d = dict.fromkeys(string.ascii_lowercase, 0)
    
    for i in urls :
        tag=i.split('=')[1].strip()
        for j in tag:
            if j.lower() in d:
                d[j.lower()]+=1
    
    for key, value in d.items():
        print('Name and Occurrance of letter:',f"{key}{value}")
    
    date_list=[]
    for i in all_dates:
        date_datetime = datetime.strptime(i, '%d/%m/%Y')
        formatted_date = date_datetime.strftime('%B %d, %Y')
        date_list.append(formatted_date)
    
    print('List of Dates:',date_list)


except Exception as e:
    print('Exception at 1',e)
