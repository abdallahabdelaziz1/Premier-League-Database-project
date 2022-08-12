from unicodedata import name
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

df_stadiums = pd.read_csv("StadiumLinks.csv")
stadiums = df_stadiums.to_dict('records')

driver = webdriver.Firefox()

driver.get('https://www.premierleague.com/')
time.sleep(5)
accept_cookies = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[1]/div[5]/button[1]')
accept_cookies.click()

stadium_table = []
did_not_work = []

limit = 10

for stadium in stadiums:
    count = 0
    while count < limit:
        count += 1
        try:
            driver.get(stadium['StadiumLink'])
            time.sleep(3)
            more_info = driver.find_element(By.XPATH, '/html/body/main/div[3]/div[2]/div/ul/li[2]')
            more_info.click()
            data = driver.find_element(By.CLASS_NAME, 'articleTabContent').find_element(By.CLASS_NAME, 'active').find_elements(By.TAG_NAME, 'p')
            capacity = record = length = width = built = 0
            address_pc = address_area = address_city = 0
            for databit in data:
                words = databit.text.split(' ')
                for i in range(len(words)):
                    if capacity == 0 and words[i].lower() == 'capacity:':
                        capacity = int(words[i+1].replace(',', ''))
                    elif record == 0 and words[i].lower() == 'attendance:':
                        record = int(words[i+1].replace(',',''))
                    elif length == 0 and words[i].lower() == 'size:':
                        length = float(words[i+1][:-1])
                        width = float(words[i+3][:-1])
                    elif built == 0 and (words[i].lower() == 'built:' or words[i].lower() == 'opened:'):
                        built = int(words[i+1])
                    elif address_pc == 0 and words[i].lower() == 'address:':
                        full_address = ' '.join(words[i+1:]).split(', ')
                        address_pc = full_address[-1]
                        address_city = full_address[-2]
                        address_area = ', '.join(full_address[:-2])
            stadium_dict = {
                "StadiumName" : stadium['StadiumName'],
                "RecordAttendence" : record,
                "DateofBuilding" : built,
                "Capacity" : capacity,
                "PitchWidth" : width,
                "PitchLength" : length,
                "AddressCity" : address_city,
                "AddressPC" : address_pc,
                "AddressArea" : address_area
            }
            print(stadium_dict)
            stadium_table.append(stadium_dict)
            break
        except:
            print('Trying', stadium['StadiumName'], 'again.')
            if count == limit:
                did_not_work.append(stadium['StadiumLink'])

print(did_not_work)
df_stadium_table = pd.DataFrame(stadium_table)
df_stadium_table.to_csv(r'StadiumTableFinal.csv', index = False)
driver.close()
