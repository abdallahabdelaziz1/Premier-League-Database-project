from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver = webdriver.Firefox()

# Seasons with their links
seasons_list = [{"season" : "2021/22", "url" : "https://www.premierleague.com/results?co=1&se=418&cl=-1"},
                {"season" : "2020/21", "url" : "https://www.premierleague.com/results?co=1&se=363&cl=-1"},
                {"season" : "2019/20", "url" : "https://www.premierleague.com/results?co=1&se=274&cl=-1"},
                {"season" : "2018/19", "url" : "https://www.premierleague.com/results?co=1&se=210&cl=-1"}]
# To click accept cockies in the first time
first_time = True
sleep_time = 5

# To store info about matches, teams, and stadiums
match_table = []
teams = []
stadiums = []

for season in seasons_list:
    driver.get(season["url"])
    time.sleep(sleep_time)

    # Accepting cockies
    if (first_time):
        accept_cookies = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[1]/div[5]/button[1]')
        accept_cookies.click()
        first_time = False
        sleep_time = 3

    # Scroll down
    current_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 	# Scroll step
        time.sleep(3) 	# Wait to load page
        try:
            new_height = driver.execute_script("return document.body.scrollHeight") # Calculate new scroll height
        except:
            print("Failed: ", new_height)
        if new_height == current_height: # Compare with last scroll height
            break
        current_height = new_height
        
    print("scorlled till",current_height)

    # Collecting match'es URLs
    matches = driver.find_elements(By.CLASS_NAME, "fixture")
    match_urls = []
    for match in matches:
        match_urls.append('https:'+ match.get_attribute('data-href'))
    
    # To monitor progress
    print("Season",season["season"])
    list_len = len(match_urls)
    print(list_len)
    m = 1

    # Collecting match data
    for url in match_urls:
        print(m, "/", list_len)
        m += 1
        while True:
            try:
                driver.get(url)
                time.sleep(1)

                stats = driver.find_element(By.XPATH,'/html/body/main/div/section[2]/div[2]/div[2]/div[1]/div/div/ul/li[3]')
                stats.click()
                time.sleep(2)

                date = driver.find_element(By.CLASS_NAME, 'renderMatchDateContainer')
                stadium = driver.find_element(By.CLASS_NAME, 'stadium')
                teams_container = driver.find_element(By.CLASS_NAME, 'teamsContainer').find_elements(By.TAG_NAME, 'div')
                home = teams_container[0].find_element(By.CLASS_NAME, 'long')
                away = teams_container[4].find_element(By.CLASS_NAME, 'long')
                score = teams_container[1].find_element(By.CLASS_NAME, 'score')
                
                # Collecting teams data
                home_url = teams_container[0].find_element(By.CLASS_NAME, 'teamName').get_attribute('href')
                home_team = {"ClubName" : home.text, "Website": home_url}
                away_url = teams_container[4].find_element(By.CLASS_NAME, 'teamName').get_attribute('href')
                away_team = {"ClubName" : away.text, "Website": away_url}
                teams.append(home_team)
                teams.append(away_team)
                print(home_team)
                print(away_team)

                # Stadium data
                stadium_dict = {"StadiumName" : stadium.text.split(',')[0].strip(), "AddressCity": stadium.text.split(',')[1].strip()}
                stadiums.append(stadium_dict)
                print(stadium_dict)

                # Match data    
                match_data = driver.find_element(By.CLASS_NAME, 'matchCentreStatsContainer').find_elements(By.TAG_NAME, 'tr')
                possession = match_data[0].find_elements(By.TAG_NAME, 'td')
                shots = match_data[2].find_elements(By.TAG_NAME, 'td')
                yellow_home = yellow_away = red_home = red_away = fouls_home = fouls_away = 0

                # To accomdate for matches with no red or yellow cards
                for i in range(len(match_data)):
                    if match_data[i].find_elements(By.TAG_NAME, 'td')[1].text == "Yellow cards":
                        yellow_home = match_data[i].find_elements(By.TAG_NAME, 'td')[0].text
                        yellow_away = match_data[i].find_elements(By.TAG_NAME, 'td')[2].text
                    elif match_data[i].find_elements(By.TAG_NAME, 'td')[1].text == "Red cards":
                        red_home = match_data[i].find_elements(By.TAG_NAME, 'td')[0].text
                        red_away = match_data[i].find_elements(By.TAG_NAME, 'td')[2].text
                    elif match_data[i].find_elements(By.TAG_NAME, 'td')[1].text == "Fouls conceded":
                        fouls_home = match_data[i].find_elements(By.TAG_NAME, 'td')[0].text
                        fouls_away = match_data[i].find_elements(By.TAG_NAME, 'td')[2].text
                break
            except:
                print("Trying", url, 'again.')
        match_dict = {
            "HomeClub" : home.text,
            "AwayClub" : away.text,
            "Season" :  season["season"],
            "MatchDate" : date.text,
            "HomeFouls" : int(fouls_home),
            "HomeGoals" : int(score.text.split('-')[0]),
            "HomeYellow" : int(yellow_home),
            "HomeRed" : int(red_home),
            "HomeShots" : int(shots[0].text),
            "HomePossession" : float(possession[0].text),
            "AwayFouls" : int(fouls_away),
            "AwayGoals" : int(score.text.split('-')[1]),
            "AwayYellow" : int(yellow_away),
            "AwayRed" : int(red_away),
            "AwayShots" : int(shots[2].text),
            "AwayPossession" : float(possession[2].text),
            "StadiumName" : stadium.text.split(',')[0].strip()
        }
        print(match_dict)
        match_table.append(match_dict)    

driver.close()

# Create DataFrames and Export CSV
df_matches = pd.DataFrame(match_table)
df_matches.to_csv(r'MatchTable.csv',index = False)

df_teams = pd.DataFrame(teams)
df_teams.drop_duplicates(inplace = True, ignore_index = True)
df_teams.to_csv(r'TeamTable.csv',index = False)

df_stadium = pd.DataFrame(stadiums)
df_stadium.drop_duplicates(inplace = True, ignore_index = True)
df_stadium.to_csv(r'StadiumTable.csv',index = False)