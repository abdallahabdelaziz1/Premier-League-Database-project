from unicodedata import name
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver = webdriver.Firefox()

# clubs_links = pd.read_csv("TeamTable.csv")
# clubs_links = clubs_links.to_dict('records')

driver.get('https://www.premierleague.com/')
time.sleep(5)
accept_cookies = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[1]/div[5]/button[1]')
accept_cookies.click()


# Seasons with their links
seasons_list = [{"season" : "2021/22", "url" : "https://www.premierleague.com/clubs?se=418"},
                {"season" : "2020/21", "url" : "https://www.premierleague.com/clubs?se=363"},
                {"season" : "2019/20", "url" : "https://www.premierleague.com/clubs?se=274"},
                {"season" : "2018/19", "url" : "https://www.premierleague.com/clubs?se=210"}]

name_stad_link = set()
for season in seasons_list:
    driver.get(season['url'])
    time.sleep(2)
    season_clubs = driver.find_element(By.CLASS_NAME, 'dataContainer').find_elements(By.TAG_NAME, 'li')
    for club in season_clubs:
        [club_name, club_stad, _] = club.text.split('\n')
        prem_link = club.find_element(By.TAG_NAME, 'a').get_attribute('href')
        
        club_tuple = (club_name, club_stad, prem_link)
        name_stad_link.add(club_tuple)

print(len(name_stad_link))

club_table = []
stadium_links = []
for club in name_stad_link:
    while True:
        try:
            driver.get(club[2])
            time.sleep(3)
            
            website = driver.find_element(By.CLASS_NAME, 'website')
            website_link = website.find_element(By.TAG_NAME, 'a').text

            stadium = driver.find_element(By.CLASS_NAME, 'stadiumName')
            stadium_link = stadium.find_element(By.TAG_NAME, 'a').get_attribute('href')
            
            stadium_dict = {
                'StadiumName' : club[1],
                'StadiumLink' : stadium_link
            }
            club_dict = {
                "ClubName": club[0],
                "Website" : website_link,
                "ClubStadium" : club[1]
            }

            club_table.append(club_dict)
            stadium_links.append(stadium_dict)
            print(club_dict)
            print(stadium_dict)
            break
        except:
            print('Trying', club[0], 'again.')

df_clubs = pd.DataFrame(club_table)
df_clubs.to_csv(r'ClubTable.csv',index = False)

df_stadiums = pd.DataFrame(stadium_links)
df_stadiums.to_csv(r'StadiumLinks.csv', index = False)
driver.close()