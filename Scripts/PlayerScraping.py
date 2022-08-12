from bs4 import BeautifulSoup
from asyncio.windows_events import NULL
from unicodedata import name
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import requests

driver = webdriver.Firefox()

driver.get('https://www.premierleague.com/')
time.sleep(6)
accept_cookies = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[1]/div[5]/button[1]')
accept_cookies.click()

# Seasons with their links
seasons_list = [{"season" : "2021/22", "url" : "https://www.premierleague.com/players?se=418&cl=-1"},
                {"season" : "2020/21", "url" : "https://www.premierleague.com/players?se=363&cl=-1"},
                {"season" : "2019/20", "url" : "https://www.premierleague.com/players?se=274&cl=-1"},
                {"season" : "2018/19", "url" : "https://www.premierleague.com/players?se=210&cl=-1"}]

season_format = ["2021/2022", "2020/2021", "2019/2020", "2018/2019"]

players_links = set()
for season in seasons_list:
    count = 0
    driver.get(season['url'])

    # Scroll down
    current_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 	# Scroll step
        time.sleep(8) 	# Wait to load page
        try:
            new_height = driver.execute_script("return document.body.scrollHeight") # Calculate new scroll height
        except:
            print("Failed: ", new_height)
        if new_height == current_height: # Compare with last scroll height
            break
        current_height = new_height
        
    print("scorlled till",current_height)

    players = driver.find_element(By.CLASS_NAME, 'dataContainer').find_elements(By.TAG_NAME, 'tr')
    for player in players:
        [player_name, _, nationality] = player.find_elements(By.TAG_NAME, 'td')
        player_link = player_name.find_element(By.TAG_NAME,'a').get_attribute('href')
        players_links.add((player_name.text, nationality.text, player_link))
        count += 1
    print(season['season'], count)
    
print(len(players_links))

player_table = []
plays_for_table = []


limit = 10
did_not_work = []
no_bdate = []
count = 1
tot = len(players_links)
for player in players_links:
    print(count, '/', tot)
    count += 1
    trials = 0
    while trials < limit:
        try:
            driver.get(player[2])
            time.sleep(2)
            player_intro = driver.find_element(By.CLASS_NAME, 'playerIntro').find_elements(By.TAG_NAME, 'div')
            position = None
            for i in range(len(player_intro)):
                if player_intro[i].text.lower() == 'position':
                    position = player_intro[i+1].text
                    break
            data = driver.find_element(By.CLASS_NAME, 'personalLists')
            all_info = data.find_elements(By.TAG_NAME, 'li')
            height = weight = bdate = None
            for info in all_info:
                if len(info.text.split('\n')) < 2:
                    continue
                [label, value] = info.text.split('\n')
                if label.lower() == 'date of birth':
                    bdate = value.split(' ')[0]
                elif label.lower() == 'height':
                    height = int(value[:-2])
                elif label.lower() == 'weight':
                    weight = value
            if weight is None:
                response = requests.get(player[2])
                html_soup: BeautifulSoup = BeautifulSoup(response.content, 'html.parser')
                weightInfo = html_soup.find(class_="u-hide") 
                if weightInfo is not None:
                    try:
                        weight = round(float(weightInfo.find(class_="info").text.replace('kg','')))
                    except:
                        weight = None
            if bdate is None:
                no_bdate.appned(player)
            player_dict = {
                'PlayerName' : player[0],
                'BirthDate' : bdate,
                'Weight' : weight,
                'Height' : height,
                'Position' : position,
                'Nationality' : player[1]
            }

            history = driver.find_element(By.CLASS_NAME, 'playerClubHistory').find_element(By.TAG_NAME, 'tbody')
            history_rows = history.find_elements(By.TAG_NAME, 'tr')
            for row in history_rows:
                if len(row.find_elements(By.TAG_NAME, 'td')) != 5:
                    continue
                [season_, club_, _, _, _] = row.find_elements(By.TAG_NAME, 'td')
                if season_.text in season_format:
                    plays_for_dict = {
                        'PlayerName' : player[0],
                        'BirthDate' : bdate,
                        'ClubName' : club_.text.replace(' (Loan)', '').replace('&', 'and').replace(' U21', '').replace(' (loan)', '').replace(' U18', ''),
                        'Season' : season_.text[:5] + season_.text[-2:]
                    }
                    print(plays_for_dict)
                    plays_for_table.append(plays_for_dict)

            player_table.append(player_dict)
            print(player_dict)
            break
        except:
            print('Trying', player[2], 'again.')
            trials += 1
            if trials == limit:
                did_not_work.append(player)

print('Did not work')
print(did_not_work)
print('No Birthdate')
print(no_bdate)
driver.close()

df_player = pd.DataFrame(player_table)
df_player.drop_duplicates(inplace = True, ignore_index = True)
df_player.to_csv(r'PlayerTable.csv', index = False)

df_plays_for = pd.DataFrame(plays_for_table)
df_plays_for.drop_duplicates(inplace = True, ignore_index = True)
df_plays_for.to_csv(r'PlaysForTable.csv', index = False)