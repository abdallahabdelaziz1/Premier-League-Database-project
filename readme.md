# Premier League Database project

## Framework

The project GUI is built using Qt 6.0+ framework. Qt is a widget toolkit for creating graphical user interfaces as well as
cross-platform applications that run on various software and hardware platforms such as Linux, Windows, macOS, Android or embedded systems.
Since the project was programmed using python, PySide6 6.3.0 module which provides access to Qt framework for python. PySide6 versions
following 6.0 use a C++ parser based on Clang. The Clang library (C-bindings), version 13.0 or higher is required for building.

## Running the project

To run the executable project include style.qss (for styling) and logo.png (for window icon) in the same directory as GUI_app.exe, then run GUI_app.exe in windows.
Not including the files is ok and the project will run; however, it won't look as nice as if you include the files.

To run the program using the source code, install the following libraries
    - mysql.connector
    - PySide6
    - datetime
    - validate_email
Then in a terminal (or cmd) run python3 GUI_app.py

## The Remote Database Hosting

The remote hosting is done using [Free MySQL Hosting](https://www.freemysqlhosting.net/)

## Navigation

The navigation is done throw the side menu. Note that to review a match, loggin in is required.
Refer to the following tree for naviagation. The tree is designed to statisfy the project requirments.

```
┌── Main Screen
├── Sign Up
├── Log in
├── Review match
├── View review (By match)
├── Player
│    ├── Show players history by nationality
│    └── Show all players for a given team position
├── Team
│    └── Show teams by city
├── Top 10
│    ├── By matches won
│    ├── By home matches won
│    ├── By yellow cards
│    ├── By fouls
│    └── By shots
├── Best of season (For the last 4 seasons)
├── Query
│    ├── Query a team
│    ├── Query a player
│    └── Identify the home team for a given stadium
└── log out
```
In the main screen there is a description for the program.
In the Sign Up screen, new users can register.
In the log in Screen, users can log in.
In the Review match Screen, logged in users can review matches by specifying the home team, away team and season.
In the View review Screen, users can see all revies by specifying a match.
In the Player Screen, users can filter players by their nationality and/or their position.
In the Team Screen, users can filter teams by their city.
In the Top 10 Screen, users can view top 10 teams by matches won, home matches won, yellow cards, fouls, shots for a given season
or for all previous 4 seasons.
In the Best of Season Screen, users can view a table of the best teams for each season by matches won.
In Query Screen, users can query a team by its name, query a player by his first/last name, query a team by its stadium name.
In Log out screen, logged in users can logout.

## Bonus requirements

1. Getting teams by city
2. GUI applications
3. Finding player by applying nationality and position filters
4. Top 10 by season and for all 4 season for all Criteria
5. The age of the player is displayed when querying a player by name

## Final Notes

- Note that if the program is left for a long time without any actions the connection to the database is lost.
  restarting the program is then required.
- Note also that more scraping was done to cover the players that are not included in the player list.
  This was done by applying a team and a season filter on the player page and then scraping players. Surprisingly, there were
  more players when following this method than scraping players only.
  To make sure no data is lost, both methods were followed and the final player and playsfor table is the union of both tables.
- Note that loans were also recorded in the plays for table.
- Note that filtering players based on nationality/position may take some time.
- Note also that for all columns the collation is case insensitive except for the password column.
- Note that when signing up, the used email needs to follow a valid format.
- Note that the dumped data is the one just before the demo.
