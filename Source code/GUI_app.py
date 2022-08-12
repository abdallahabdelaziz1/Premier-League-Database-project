# imports
import sys
import mysql.connector
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from datetime import date
from validate_email import validate_email

class session(QDialog):

    def __init__(self, parent = None):
        super(session, self).__init__(parent)

        # Conncting to database
        self.connect_to_database()
        # Creating necessary views
        self.create_views()

        # Current user data
        self.useremail = None
        self.username = None

        self.all_clubs = [
            "Chelsea", "Aston Villa", "Newcastle United", "West Ham United",
            "Sheffield United", "Cardiff City", "Brentford", "Brighton and Hove Albion",
            "Southampton", "Watford" , "Everton", "Leicester City", "Tottenham Hotspur",
            "Norwich City", "West Bromwich Albion", "Huddersfield Town", "Crystal Palace", 
            "AFC Bournemouth", "Wolverhampton Wanderers", "Arsenal", "Fulham",
            "Manchester United", "Liverpool" , "Burnley", "Leeds United", "Manchester City"
        ]

        self.all_seasons = ['2018/19', '2019/20', '2020/21', '2021/22']

        ### UI components

        # Setting the icon
        self.setWindowIcon(QIcon('logo.png'))

        # Setting window size and title
        self.setFixedSize(1000, 600)
        self.setWindowTitle("Premier League")

        # Creating Side Menu
        self.menu_widget = QListWidget()
        self.menu_widget.setFixedWidth(150)
        self.fill_menu()



        # Creating Layouts
        self.main_menu_widget = QWidget()
        self.create_main_menu()
        self.signin_widget = QWidget()
        self.create_signin_layout()
        self.signup_widget = QWidget()
        self.create_signup_layout()
        self.review_match_widget = QWidget()
        self.create_review_match_layout()
        self.view_review_widget = QWidget()
        self.create_view_review_layout()
        self.player_widget = QWidget()
        self.create_player_layout()
        self.team_widget = QWidget()
        self.create_team_layout()
        self.top10_widget = QWidget()
        self.create_top10_layout()
        self.best_of_season_widget = QWidget()
        self.create_best_of_season_layout()
        self.query_widget = QWidget()
        self.create_query_layout()
        self.logout_widget = QWidget()
        self.create_logout_layout()

        # Adding layouts to QStackedWidget
        self.all_layouts = QStackedWidget(self)
        self.all_layouts.addWidget(self.main_menu_widget)
        self.all_layouts.addWidget(self.signup_widget)
        self.all_layouts.addWidget(self.signin_widget)
        self.all_layouts.addWidget(self.review_match_widget)
        self.all_layouts.addWidget(self.view_review_widget)
        self.all_layouts.addWidget(self.player_widget)
        self.all_layouts.addWidget(self.team_widget)
        self.all_layouts.addWidget(self.top10_widget)
        self.all_layouts.addWidget(self.best_of_season_widget)
        self.all_layouts.addWidget(self.query_widget)
        self.all_layouts.addWidget(self.logout_widget)
        

        # Connecting QListWidget to QStackedWidget
        self.menu_widget.itemClicked.connect(self.layout_manager)

        # Window
        hbox = QHBoxLayout(self)
        hbox.addWidget(self.menu_widget)
        hbox.addWidget(self.all_layouts)

        self.setLayout(hbox)

    # Creating layouts
    def create_main_menu(self):
        welcome = "Welcome!"
        self.welcome_label = QLabel(welcome)
        desc_txt = """
In the Sign Up screen, new users can register.
In the log in Screen, registered users can log in.
In the Review match Screen, logged in users can review matches by specifying the home team, away team and season.
In the View review Screen, users can see all revies by specifying a match.
In the Player Screen, users can filter players by their nationality and/or their position.
In the Team Screen, users can filter teams by their city.
In the Top 10 Screen, users can view top 10 teams by matches won, home matches won, yellow cards, fouls, shots for a given season
or for the previous 4 seasons.
In the Best of Season Screen, users can view a table of the best teams for each season by matches won.
In Query Screen, users can query a team by its name, query a player by his first/last name, query a team by its stadium name.
In Log out screen, logged in users can logout.
        """
        desc_label = QLabel(desc_txt)
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel(""))
        main_layout.addWidget(self.welcome_label)
        main_layout.addWidget(desc_label)
        main_layout.addWidget(QLabel(""))
        self.main_menu_widget.setLayout(main_layout)

    def create_signup_layout(self):
        # Form part of sign up
        form_layout = QFormLayout()

        # email
        self.signup_email = QLineEdit()
        form_layout.addRow("Email:", self.signup_email)

        # username
        self.signup_username = QLineEdit()
        form_layout.addRow("Username:", self.signup_username)

        # password
        self.signup_pw = QLineEdit()
        self.signup_pw.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Password:", self.signup_pw)

        # birthdate
        self.calendar = QCalendarWidget()
        self.calendar.setLocale(QLocale.English)
        self.calendar.setGridVisible(True)
        self.calendar.setMaximumDate(QDate(2014, 12, 31))
        self.calendar.setMinimumDate(QDate(1922, 1, 1))
        form_layout.addRow("Birthdate:\n(Default is 31/12/2014)", self.calendar)

        # favorite club
        self.fav_club = QComboBox()
        self.fav_club.addItems(self.all_clubs)
        form_layout.addRow("Favourite Club:", self.fav_club)

        # Gender
        self.button_group = QButtonGroup()
        self.male_button = QRadioButton("Male")
        self.female_button = QRadioButton("Female")
        self.button_group.addButton(self.male_button, 1)
        self.button_group.addButton(self.female_button, 2)
        
        group_box = QGroupBox("Gender")
        hbox = QHBoxLayout()
        hbox.addWidget(self.male_button)
        hbox.addWidget(self.female_button)
        group_box.setLayout(hbox)
        
        # Status label
        self.signup_label = QLabel()
        self.signup_label.setText("")

        # Sumbit button
        submit = QPushButton("Register")
        submit.clicked.connect(self.signup_submit)

        # Final layout
        signup_layout = QVBoxLayout()
        signup_layout.addLayout(form_layout)
        signup_layout.addWidget(group_box)
        signup_layout.addWidget(self.signup_label)
        signup_layout.addWidget(submit)

        self.signup_widget.setLayout(signup_layout)

    def create_signin_layout(self):
        # Form part of sign in
        form_layout = QFormLayout()

        # email
        self.signin_email = QLineEdit()
        form_layout.addRow("Email:", self.signin_email)

        # password
        self.signin_pw = QLineEdit()
        self.signin_pw.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Password:", self.signin_pw)
        
        # Status label
        self.signin_label = QLabel()
        self.signin_label.setText("")

        # Sumbit button
        self.login_submit = QPushButton("Sign in")
        self.login_submit.clicked.connect(self.signin_submit)

        # Final layout
        signin_layout = QVBoxLayout()
        signin_layout.addLayout(form_layout)
        signin_layout.addWidget(self.signin_label)
        signin_layout.addWidget(self.login_submit)

        self.signin_widget.setLayout(signin_layout)

    def create_review_match_layout(self):
        # Form parts of review match
        form_layout_1 = QFormLayout()
        form_layout_2 = QFormLayout()
        form_layout_3 = QFormLayout()

        # home
        self.review_home = QComboBox()
        self.review_home.addItems(self.all_clubs)
        form_layout_1.addRow("Home Club: ", self.review_home)

        # away
        self.review_away = QComboBox()
        self.review_away.addItems(self.all_clubs)
        form_layout_2.addRow("Away Club: ", self.review_away)

        # season
        self.review_season = QComboBox()
        self.review_season.addItems(self.all_seasons)
        form_layout_3.addRow("Season: ", self.review_season)

        review_form = QFormLayout()

        # rating   
        self.rating = QSpinBox()    
        self.rating.setRange(0,10)
        self.rating.setLocale(QLocale.English)
        review_form.addRow("Rating:", self.rating)

        # reivew
        self.review = QTextEdit()
        review_form.addRow("Reivew: ", self.review)

        # Status label
        self.review_label = QLabel()
        self.review_label.setText("")

        # Sumbit button
        self.review_submit_button = QPushButton("Post Review")
        self.review_submit_button.clicked.connect(self.review_submit)
        self.review_submit_button.setEnabled(False)

        # form layout
        input_layout = QHBoxLayout()
        input_layout.addLayout(form_layout_1)
        input_layout.addLayout(form_layout_2)
        input_layout.addLayout(form_layout_3)
        
        # Final layout
        review_layout = QVBoxLayout()
        review_layout.addLayout(input_layout)
        review_layout.addLayout(review_form)
        review_layout.addWidget(self.review_label)
        review_layout.addWidget(self.review_submit_button)

        self.review_match_widget.setLayout(review_layout)

    def create_view_review_layout(self):
        # Form parts of review match
        form_layout_1 = QFormLayout()
        form_layout_2 = QFormLayout()
        form_layout_3 = QFormLayout()

        # home
        self.view_home = QComboBox()
        self.view_home.addItems(self.all_clubs)
        form_layout_1.addRow("Home Club: ", self.view_home)

        # away
        self.view_away = QComboBox()
        self.view_away.addItems(self.all_clubs)
        form_layout_2.addRow("Away Club: ", self.view_away)

        # season
        self.view_season = QComboBox()
        self.view_season.addItems(['2018/19', '2019/20', '2020/21', '2021/22'])
        form_layout_3.addRow("Season: ", self.view_season)

        # choose match
        submit = QPushButton("Choose Match")
        submit.clicked.connect(self.get_reviews)

        # reviews
        self.review_scroll_area = QScrollArea()
        self.review_scroll_area.hide()

        # form layout
        input_layout = QHBoxLayout()
        input_layout.addLayout(form_layout_1)
        input_layout.addLayout(form_layout_2)
        input_layout.addLayout(form_layout_3)

        # Final layout
        view_layout = QVBoxLayout()
        view_layout.addLayout(input_layout)
        view_layout.addWidget(self.review_scroll_area)
        view_layout.addWidget(submit)

        self.view_review_widget.setLayout(view_layout)

    def create_player_layout(self):
        # Taking user criteria
        self.player_button_group = QButtonGroup()
        self.include_nationality = QCheckBox("Nationality")
        self.include_position = QCheckBox("Position")
        self.player_button_group.addButton(self.include_nationality, 1)
        self.player_button_group.addButton(self.include_position, 2)
        self.player_button_group.setExclusive(False)
        self.player_group_box = QGroupBox("Criteria")
        hbox = QHBoxLayout()
        hbox.addWidget(self.include_nationality)
        hbox.addWidget(self.include_position)
        self.player_group_box.setLayout(hbox)

        # Taking user input
        self.player_nationality = QLineEdit()
        self.player_position = QComboBox()
        positions = ['Forward', 'Defender', 'Midfielder', 'Goalkeeper']
        self.player_position.addItems(positions)
        temp_form_1 = QFormLayout()
        temp_form_1.addRow("Nationlity", self.player_nationality)
        temp_form_2 = QFormLayout()
        temp_form_2.addRow("Position", self.player_position)

        # Input form
        hbox2 = QHBoxLayout()
        hbox2.addLayout(temp_form_1)
        hbox2.addLayout(temp_form_2)

        # Other components
        self.player_scroll_area = QScrollArea()
        submit = QPushButton("Get Players")
        submit.clicked.connect(self.get_player)

        # Final layout
        player_layout = QVBoxLayout()
        player_layout.addWidget(self.player_group_box)
        player_layout.addLayout(hbox2)
        player_layout.addWidget(self.player_scroll_area)
        player_layout.addWidget(submit)

        self.player_widget.setLayout(player_layout)
        

    def create_team_layout(self):
        # form component
        self.team_city = QLineEdit()
        form = QFormLayout()
        form.addRow("City", self.team_city)

        # other components
        self.team_scroll = QScrollArea()

        team_submit = QPushButton("Get teams")
        team_submit.clicked.connect(self.get_teams)

        # Final layout
        team_layout = QVBoxLayout()
        team_layout.addLayout(form)
        team_layout.addWidget(self.team_scroll)
        team_layout.addWidget(team_submit)

        self.team_widget.setLayout(team_layout)

    def create_top10_layout(self):
        # Form layouts
        form_layout_1 = QFormLayout()
        form_layout_2 = QFormLayout()

        # Choose Season
        self.top10_season = QComboBox()
        self.top10_season.addItems(self.all_seasons)
        self.top10_season.addItem("All Seasons")
        form_layout_1.addRow("Season:", self.top10_season)

        # Choose Criteria
        self.top10_criteria = QComboBox()
        self.top10_criteria.addItems(["Matches won", "Home Matches won", "Yellow cards", "Fouls", "Shots"])
        form_layout_2.addRow("Criteria:", self.top10_criteria)

        # input layout
        hbox = QHBoxLayout()
        hbox.addLayout(form_layout_1)
        hbox.addLayout(form_layout_2)

        # Table of results
        self.top10_table = QTableWidget(10,3)
        self.top10_table.hide()

        # Submit button
        submit = QPushButton("Submit")
        submit.clicked.connect(self.top10_submit)

        # Final Layout
        top10_layout = QVBoxLayout()
        top10_layout.addLayout(hbox)
        top10_layout.addWidget(self.top10_table)
        top10_layout.addWidget(submit)

        self.top10_widget.setLayout(top10_layout)

    def create_best_of_season_layout(self):
        # Best of Seasons table
        self.best_table = QTableWidget()

        sql = """
        SELECT A.ClubName, A.Season, A.Wins
        FROM allWins A INNER JOIN maxWins M
        ON A.Season = M.Season AND A.Wins = M.Wins
        ORDER BY A.Season;
        """

        self.mycursor.execute(sql)
        best = self.mycursor.fetchall()
    
        self.best_table.setFixedSize(340, 170)

        # Filling the table
        self.best_table.setRowCount(len(best))
        self.best_table.setColumnCount(3)
        self.best_table.setHorizontalHeaderLabels(["Club", "Season", "Wins"])


        for i in range(len(best)):
            for j in range(3):
                self.best_table.setCellWidget(i, j, QLabel(str(best[i][j])))

        # Final Layout
        best_layout = QVBoxLayout()
        best_layout.addWidget(QLabel(""))
        best_layout.addWidget(QLabel("<strong>The Best of the Previous Four Seasons are</strong>", alignment = Qt.AlignHCenter))
        best_layout.addWidget(self.best_table, alignment=Qt.AlignHCenter)
        best_layout.addWidget(QLabel(""))
        best_layout.addWidget(QLabel(""))

        self.best_of_season_widget.setLayout(best_layout)

    def create_query_layout(self):
        # Choosing the query
        form_layout = QFormLayout()
        self.query = QComboBox()
        self.query.addItems(["Query a club", "Query a player", "Identify the home team by stadium"])
        self.query.activated.connect(self.switch_query_page)
        form_layout.addRow("Select a Query:", self.query)

        self.query_stacked = QStackedWidget()

        # Query a team page
        page1 = QWidget()
        page1_layout = QVBoxLayout()
        page1_form= QFormLayout()
        self.query_club_name = QLineEdit()
        page1_form.addRow("Club Name:", self.query_club_name)
        team_grid = QVBoxLayout()
        team_submit = QPushButton("Get Club")
        team_submit.clicked.connect(self.query_team_submit)
        page1_layout.addLayout(page1_form)
        page1_layout.addLayout(team_grid)
        page1_layout.addWidget(team_submit)
        page1.setLayout(page1_layout)

        self.res_teamname = QLabel("")
        self.res_teamlink = QLabel("")
        self.res_teamlink.setOpenExternalLinks(True)
        self.res_teamstad = QLabel("")
        self.res_teamcity = QLabel("")

        team_grid.addWidget(self.res_teamname)
        team_grid.addWidget(self.res_teamlink)
        team_grid.addWidget(self.res_teamstad)
        team_grid.addWidget(self.res_teamcity)
        team_grid.addWidget(QLabel(""))
        team_grid.addWidget(QLabel(""))
        team_grid.addWidget(QLabel(""))


        
        # Query a player name
        page2 = QWidget()
        page2_layout = QVBoxLayout()
        page2_form = QFormLayout()
        self.query_player_name = QLineEdit()
        page2_form.addRow("Player Name (First and Last):", self.query_player_name)
        player_grid = QVBoxLayout()
        player_submit = QPushButton("Get Player")
        player_submit.clicked.connect(self.query_palyer_submit)
        page2_layout.addLayout(page2_form)
        page2_layout.addLayout(player_grid)
        page2_layout.addWidget(player_submit)
        page2.setLayout(page2_layout)

        self.playsfor_table = QTableWidget()
        self.playsfor_table.hide()

        self.res_playername = QLabel("")
        self.res_playerbd = QLabel("")
        self.res_playerage = QLabel("")
        self.res_playerweight = QLabel("")
        self.res_playerheight = QLabel("")
        self.res_playerpos = QLabel("")
        self.res_playernat = QLabel("")

        player_grid.addWidget(self.res_playername)
        player_grid.addWidget(self.res_playerbd)
        player_grid.addWidget(self.res_playerage)
        player_grid.addWidget(self.res_playerweight)
        player_grid.addWidget(self.res_playerheight)
        player_grid.addWidget(self.res_playerpos)
        player_grid.addWidget(self.res_playernat)
        player_grid.addWidget(self.playsfor_table)
        player_grid.addWidget(QLabel(""))
        player_grid.addWidget(QLabel(""))


        # Query a club by stadium
        page3 = QWidget()
        page3_layout = QVBoxLayout()
        page3_form = QFormLayout()
        self.query_stad_name = QLineEdit()
        page3_form.addRow("Stadium Name:", self.query_stad_name)
        club_grid = QVBoxLayout()
        stad_submit = QPushButton("Get Club")
        stad_submit.clicked.connect(self.query_stad_submit)
        page3_layout.addLayout(page3_form)
        page3_layout.addLayout(club_grid)
        page3_layout.addWidget(stad_submit)
        page3.setLayout(page3_layout)


        self.resstadname = QLabel("")
        self.restadwebsite = QLabel("")
        self.resstadstad = QLabel("")
        self.resstadcity = QLabel("")


        club_grid.addWidget(self.resstadname)
        club_grid.addWidget(self.restadwebsite)
        club_grid.addWidget(self.resstadstad)
        club_grid.addWidget(self.resstadcity)
        club_grid.addWidget(QLabel(""))
        club_grid.addWidget(QLabel(""))
        club_grid.addWidget(QLabel(""))


        self.query_stacked.addWidget(page1)
        self.query_stacked.addWidget(page2)
        self.query_stacked.addWidget(page3)

        # Final layout
        query_layout = QVBoxLayout()
        query_layout.addLayout(form_layout)
        query_layout.addWidget(self.query_stacked)

        self.query_widget.setLayout(query_layout)

    def create_logout_layout(self):
        self.logout_label = QLabel("You are not logged in!")
        self.logout_button = QPushButton("Logout")
        self.logout_button.setEnabled(False)
        self.logout_button.clicked.connect(self.logout_submit)

        # Final Layout
        logout_layout = QVBoxLayout()
        logout_layout.addWidget(self.logout_label)
        logout_layout.addWidget(self.logout_button)

        self.logout_widget.setLayout(logout_layout)

    # Slots
    @Slot()
    def signup_submit(self):
        # Dictionary to store user data
        user_dict = {}
        if not self.my_validate_email(self.signup_email.text()):
            return
        user_dict['email'] = self.signup_email.text()

        if len(self.signup_username.text()) == 0:
            self.signup_label.setText("Please enter a username!")
            return
        user_dict['username'] = self.signup_username.text()

        if len(self.signup_pw.text()) == 0:
            self.signup_label.setText("Please enter a password!")
            return
        user_dict['password'] = self.signup_pw.text()

        user_dict['bdate'] = self.calendar.selectedDate().toString(Qt.ISODateWithMs)
        
        user_dict['favClub'] = self.fav_club.currentText()

        if self.button_group.checkedButton() == None:
            self.signup_label.setText("Please select a gender!")
            return
        user_dict['gender'] = self.button_group.checkedButton().text()[0]
        
        # Putting values in tuple format
        values = (user_dict['email'], user_dict['password'], user_dict['username'], user_dict['gender'], user_dict['favClub'], user_dict['bdate'])

        self.db_insert('fan', values)
        # print(Fore.GREEN + "Congratulations, your account has been successfully created.")
        # print(Fore.WHITE)
        msgBox = QMessageBox()
        msgBox.setText("Congratulations, your account has been created successfully.")
        msgBox.exec()

        # reseting the form
        self.signup_label.setText("")
        self.signup_email.clear()
        self.signup_pw.clear()
        self.signup_username.clear()
        self.button_group.setExclusive(False)
        self.male_button.setChecked(False)
        self.female_button.setChecked(False)
        self.button_group.setExclusive(True)

    @Slot()
    def signin_submit(self):
        # validate sign in credentials
        sql = """SELECT * FROM `fan` WHERE `Password` = "{}" AND `Email` = "{}";"""
        sql = sql.format(self.signin_pw.text(), self.signin_email.text())
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        if len(myresult) == 0:
            self.signin_label.setText('<p style="color:red; text-align:justify;"><center><strong>Wrong Credentials</strong></center></p>')
            return

        self.signin_label.setText('<p style="color:green; text-align:justify;"><center><strong>Login Successful</strong></center></p>')

        # Storing login credentials of current user
        self.username = myresult[0][2]
        self.useremail = myresult[0][0]

        self.logged_in_state()

    @Slot()
    def review_submit(self):
        home = self.review_home.currentText()
        away = self.review_away.currentText()
        season = self.review_season.currentText()
        if not self.validate_match(home, away, season):
            return
        rating = self.rating.value()
        review = self.review.toPlainText().strip()
        if len(review) == 0:
            no_rev = QMessageBox()
            no_rev.setText("Please type a review")
            no_rev.exec()
            return
        values = (self.useremail, home, away, season, rating, review)
        try:
            self.db_insert("matchreview", values)
            scs = QMessageBox()
            scs.setText("Recorded Successfully")
            scs.exec()
            self.rating.setValue(0)
            self.review.setPlainText("")
        except:
            fail = QMessageBox()
            fail.setText("Recorded Successfully")
            fail.exec()

        
    @Slot()
    def get_reviews(self):
        self.fill_scroll_review()
        self.review_scroll_area.show()
        
    @Slot()
    def get_player(self):
        sql = """
            SELECT P.PlayerName, P.BirthDate, P.Weight, P.Height, P.Position, P.Nationality, PF.ClubName, PF.Season
            FROM player P INNER JOIN playsfor PF
            ON P.PlayerName = PF.PlayerName AND P.BirthDate = PF.BirthDate
            {};
        """
        added = None
        nat = self.player_nationality.text()
        pos = self.player_position.currentText()

        if self.include_nationality.isChecked() and self.include_position.isChecked():
            added = "WHERE P.Nationality = '{}' AND P.Position = '{}'"
            added = added.format(nat, pos)
        elif not self.include_nationality.isChecked() and self.include_position.isChecked():
            added = "WHERE P.Position = '{}'"
            added = added.format(pos)
        elif self.include_nationality.isChecked() and  not self.include_position.isChecked():
            added = "WHERE P.Nationality = '{}'"
            added = added.format(nat)
        else:
            no_criteria = QMessageBox()
            no_criteria.setText("Please specify a critera!")
            no_criteria.exec()
            return
        
        sql = sql.format(added)

        self.mycursor.execute(sql)
        players = self.mycursor.fetchall()

        self.player_table = QTableWidget(len(players), 8)
        self.player_table.setFixedSize(900, 500)

        column_labels = ["PlayerName", "BirthDate", "Weight", "Height", "Position", "Nationality", "ClubName", "Season"]
        self.player_table.setHorizontalHeaderLabels(column_labels)


        for i in range(len(players)):
            for j in range(8):
                self.player_table.setCellWidget(i, j, QLabel(str(players[i][j])))

        self.player_scroll_area.setWidget(self.player_table)

    @Slot()
    def get_teams(self):
        town_dict = {
            "burnley" : "Lancashire",
            "Watford" : "Hertfordshire", 
            "Newcastle" : "Newcastle Upon Tyne",
            "Sheffield" : "South Yorkshire",
            "West Bromwich" : "West Midlands"
        }
        city = self.team_city.text().strip()
        if len(city) == 0:
            no_criteria = QMessageBox()
            no_criteria.setText("Please specify a city!")
            no_criteria.exec()
            return

        if city in town_dict.keys():
            city =  town_dict[city]

        sql = """
            SELECT C.ClubName, C.Website, S.StadiumName, S.AddressCity
            FROM stadium S INNER JOIN club C
            ON C.ClubStadium = S.StadiumName
            WHERE S.AddressCity = "{}";
        """.format(city)

        self.mycursor.execute(sql)
        clubs = self.mycursor.fetchall()

        clubs_table = QTableWidget(len(clubs), 4)
        clubs_table.setFixedSize(900, 500)
        clubs_table.setHorizontalHeaderLabels(["Club", "Website", "Stadium Name", "City"])

        for i in range(len(clubs)):
                for j in range(4):
                    if j == 1:
                        link = QLabel("<a href = {}>{}</a>".format(clubs[i][j], clubs[i][j]))
                        link.setOpenExternalLinks(True)
                        clubs_table.setCellWidget(i, j , link)
                    else:
                        clubs_table.setCellWidget(i, j , QLabel(str(clubs[i][j])))

        self.team_scroll.setWidget(clubs_table)

    @Slot()
    def top10_submit(self):
        columnLabels = ["Club Name","Season", self.top10_criteria.currentText()]
        self.top10_table.setHorizontalHeaderLabels(columnLabels)

        # SQL dictionary key->criteria, value->sql
        sql_dict = {
            "Matches won" : """
                SELECT C.ClubName{}, SUM(CASE
                    WHEN C.ClubName = M.HomeClub AND M.HomeGoals > M.AwayGoals THEN 1
                    WHEN C.ClubName = M.AwayClub AND M.AwayGoals > M.HomeGoals THEN 1
                    ELSE 0
                END) AS Wins
                FROM club C INNER JOIN `match` M
                ON C.ClubName = M.HomeClub OR C.ClubName = M.AwayClub
                {}
                GROUP BY C.ClubName
                ORDER BY Wins DESC
                LIMIT 10;
            """, 
            "Home Matches won": """
                SELECT C.ClubName{}, 
                SUM(CASE
                    WHEN M.HomeGoals > M.AwayGoals THEN 1
                    ELSE 0
                END) AS HomeWins
                FROM club C INNER JOIN `match` M
                ON C.ClubName = M.HomeClub
                {}
                GROUP BY C.ClubName
                ORDER BY HomeWins DESC
                LIMIT 10;
            """, 
            "Yellow cards" : """
                SELECT C.ClubName{}, 
                SUM(CASE
                    WHEN C.ClubName = M.HomeClub THEN M.HomeYellow
                    WHEN C.ClubName = M.AwayClub THEN M.AwayYellow
                    ELSE 0
                END) AS YellowCards
                FROM club C INNER JOIN `match` M
                ON C.ClubName = M.HomeClub OR C.ClubName = M.AwayClub
                {}
                GROUP BY C.ClubName
                ORDER BY YellowCards DESC
                LIMIT 10;
            """,
            "Fouls" : """
                SELECT C.ClubName{}, 
                SUM(CASE
                    WHEN C.ClubName = M.HomeClub THEN M.HomeFouls
                    WHEN C.ClubName = M.AwayClub THEN M.AwayFouls
                    ELSE 0
                END) AS Fouls
                FROM club C INNER JOIN `match` M
                ON C.ClubName = M.HomeClub OR C.ClubName = M.AwayClub
                {}
                GROUP BY C.ClubName
                ORDER BY Fouls DESC
                LIMIT 10;
            """,
            "Shots" : """
                SELECT C.ClubName{}, 
                SUM(CASE
                    WHEN C.ClubName = M.HomeClub THEN M.HomeShots
                    WHEN C.ClubName = M.AwayClub THEN M.AwayShots
                    ELSE 0
                END) AS Shots
                FROM club C INNER JOIN `match` M
                ON C.ClubName = M.HomeClub OR C.ClubName = M.AwayClub
                {}
                GROUP BY C.ClubName
                ORDER BY Shots DESC
                LIMIT 10;
            """
        }

        sql = None
        if self.top10_season.currentText() == "All Seasons":
            sql = sql_dict[self.top10_criteria.currentText()].format("","")
        else:
            sql = sql_dict[self.top10_criteria.currentText()].format(", M.Season", "WHERE M.Season = '{}'".format(self.top10_season.currentText()))

        self.mycursor.execute(sql)
        res = self.mycursor.fetchall()

        # Filling table
        if self.top10_season.currentText() == "All Seasons":
            for i in range(10):
                self.top10_table.setCellWidget(i, 0, QLabel(res[i][0]))
                self.top10_table.setCellWidget(i, 1, QLabel("All Seasons"))
                self.top10_table.setCellWidget(i, 2, QLabel(str(res[i][1])))
        else:
            for i in range(10):
                for j in range(3):
                    self.top10_table.setCellWidget(i, j , QLabel(str(res[i][j])))

        self.top10_table.show()

    @Slot()
    def query_team_submit(self):
        name = self.query_club_name.text().strip()

        # Validating the user specified an input
        if len(name) == 0:
            no_criteria = QMessageBox()
            no_criteria.setText("Please specify a name!")
            no_criteria.exec()
            return


        sql = """
            SELECT C.ClubName, C.Website, S.StadiumName, S.AddressCity
            FROM stadium S INNER JOIN club C
            ON C.ClubStadium = S.StadiumName
            WHERE C.ClubName = "{}";
        """.format(name)

        self.mycursor.execute(sql)
        club = self.mycursor.fetchall()

        if len(club) == 0:
            no_result = QMessageBox()
            no_result.setText("A Club with this name doesn't exist!")
            no_result.exec()
            return

        
        self.res_teamname.setText("<strong>Club Name:</strong> {}".format(club[0][0]))
        self.res_teamlink.setText("<strong>Website:</strong> <a href = '{}'>{}</a>".format(club[0][1], club[0][1]))
        self.res_teamstad.setText("<strong>Stadium Name:</strong> {}".format(club[0][2]))
        self.res_teamcity.setText("<strong>City:</strong> {}".format(club[0][3]))


    @Slot()
    def query_palyer_submit(self):
        name = self.query_player_name.text().strip()
        if len(name) == 0:
            no_criteria = QMessageBox()
            no_criteria.setText("Please specify a name!")
            no_criteria.exec()
            return

        sql = """
            SELECT *
            FROM player
            WHERE PlayerName = "{}";
        """.format(name)

        sql2 = """
            SELECT *
            FROM playsfor
            WHERE PlayerName = "{}";
        """.format(name)

        self.mycursor.execute(sql)
        player = self.mycursor.fetchall()


        if len(player) == 0:
            no_result = QMessageBox()
            no_result.setText("A player with this name doesn't exist!")
            no_result.exec()
            return

        # Computing player age
        today = date.today()
        born = player[0][1]
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

        # Fillaing player date
        self.res_playername.setText("<strong>Player Name:</strong> {}".format(player[0][0]))
        self.res_playerbd.setText("<strong>Birthdate:</strong> {}".format(player[0][1]))
        self.res_playerage.setText("<strong>Age:</strong> {}".format(age))
        self.res_playerweight.setText("<strong>Weight:</strong> {}".format(player[0][2]))
        self.res_playerheight.setText("<strong>Height:</strong> {}".format(player[0][3]))
        self.res_playernat.setText("<strong>Position:</strong> {}".format(player[0][4]))
        self.res_playerpos.setText("<strong>Nationality:</strong> {}".format(player[0][5]))

        self.mycursor.execute(sql2)
        playsfor = self.mycursor.fetchall()

        # Fill table
        self.playsfor_table.setRowCount(len(playsfor))
        self.playsfor_table.setColumnCount(2)
        self.playsfor_table.setHorizontalHeaderLabels(["Season", "ClubName"])


        for i in range(len(playsfor)):
            self.playsfor_table.setCellWidget(i, 0, QLabel(str(playsfor[i][3])))
            self.playsfor_table.setCellWidget(i, 1, QLabel(str(playsfor[i][2])))

        self.playsfor_table.show()

    @Slot()
    def query_stad_submit(self):
        name = self.query_stad_name.text().strip()
        if len(name) == 0:
            no_criteria = QMessageBox()
            no_criteria.setText("Please specify a name!")
            no_criteria.exec()
            return


        sql = """
            SELECT C.ClubName, C.Website, S.StadiumName, S.AddressCity
            FROM stadium S INNER JOIN club C
            ON C.ClubStadium = S.StadiumName
            WHERE C.ClubStadium = "{}";
        """.format(name)

        self.mycursor.execute(sql)
        club = self.mycursor.fetchall()


        if len(club) == 0:
            no_result = QMessageBox()
            no_result.setText("A Club with this name doesn't exist!")
            no_result.exec()
            return 


        self.resstadname.setText("<strong>Club Name:</strong> {}".format(club[0][0]))
        self.restadwebsite.setText("<strong>Website:</strong> <a href = '{}'>{}</a>".format(club[0][1], club[0][1]))
        self.resstadstad.setText("<strong>Stadium Name:</strong> {}".format(club[0][2]))
        self.resstadcity.setText("<strong>City:</strong> {}".format(club[0][3]))

    @Slot()
    def logout_submit(self):
        self.username = None
        self.useremail = None

        self.logged_out_state()

    # Helper functions
    def fill_scroll_review(self):
        temp = QWidget()
        temp_layout = QVBoxLayout()

        home = self.view_home.currentText()
        away = self.view_away.currentText()
        season = self.view_season.currentText()

        sql = """
            SELECT F.UserName, M.Rating, M.ReviewText
            FROM `matchreview` M INNER JOIN `fan` F
            ON M.FanEmail = F.Email
            WHERE `HomeClub` = "{}" AND `AwayClub` = "{}" AND `Season` = "{}";
        """.format(home, away, season)

        self.mycursor.execute(sql)
        results = self.mycursor.fetchall()

        if len(results) == 0:
            err = QMessageBox()
            err.setText("No reviews are available for this match!")
            err.exec()
            return

        for result in results:
            tempg = QGroupBox(result[0])
            templ = QVBoxLayout()
            templ.addWidget(QLabel("<strong>Rating:</strong> {}".format(result[1])))
            templ.addWidget(QLabel(result[2]))
            tempg.setLayout(templ)
            temp_layout.addWidget(tempg)


        temp.setLayout(temp_layout)
        self.review_scroll_area.setWidget(temp)

    def my_validate_email(self, email):
        # check email structure
        is_valid = validate_email(email)
        if not is_valid:
            self.signup_label.setText("Please enter a valid email")
            return False
        
        # check if email already exists
        sql = """SELECT * FROM `fan` WHERE `Email` = "{}";""".format(email)
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        if len(myresult) != 0:
            # print(Fore.RED + "This email is already used!")
            # print(Fore.WHITE)
            self.signup_label.setText("This email is already used")
            return False
        return True

    def db_insert(self, table, values):
        sql = """INSERT INTO `{}` VALUES {};""".format(table, str(values))
        self.mycursor.execute(sql)
        self.db.commit()

    def connect_to_database(self):
        self.db = mysql.connector.connect(
            host = "sql4.freemysqlhosting.net",
            user = "sql4485961", 
            password = "wRPKSmidXR"
        )
        self.mycursor = self.db.cursor()
        sql_db = """USE sql4485961;"""
        self.mycursor.execute(sql_db)

    def create_views(self):
        sql = """
        CREATE OR REPLACE VIEW allWins
        AS SELECT C.ClubName, M.Season, SUM(CASE
            WHEN C.ClubName = M.HomeClub AND M.HomeGoals > M.AwayGoals THEN 1
            WHEN C.ClubName = M.AwayClub AND M.AwayGoals > M.HomeGoals THEN 1
            ELSE 0
        END) AS Wins
        FROM club C INNER JOIN `match` M
        ON C.ClubName = M.HomeClub OR C.ClubName = M.AwayClub
        GROUP BY C.ClubName, M.Season;
        """
        sql2 = """
        CREATE OR REPLACE VIEW maxWins
        AS SELECT Season, MAX(Wins) AS Wins
        FROM allWins
        GROUP BY Season;
        """
        self.mycursor.execute(sql)
        self.mycursor.execute(sql2)
        

    def fill_menu(self):
        items = []
        items.append(QListWidgetItem("Main Screen"))
        items.append(QListWidgetItem("Register"))
        items.append(QListWidgetItem("Log in"))
        items.append(QListWidgetItem("Review Match"))
        items.append(QListWidgetItem("View Reviews"))
        items.append(QListWidgetItem("Player"))
        items.append(QListWidgetItem("Team"))
        items.append(QListWidgetItem("Top 10"))
        items.append(QListWidgetItem("Best of Season"))
        items.append(QListWidgetItem("Query"))
        items.append(QListWidgetItem("Log out"))

        idx = 0
        self.item_index_map = {}
        for item in items:
            self.item_index_map[item.text()] = idx
            item.setTextAlignment(Qt.AlignCenter)
            self.menu_widget.addItem(item)
            if item.text() == "Main Screen":
                self.menu_widget.setCurrentItem(item)
            idx += 1

    def layout_manager(self, item):
        self.all_layouts.setCurrentIndex(self.item_index_map[item.text()])

    def switch_query_page(self):
        self.query_stacked.setCurrentIndex(self.query.currentIndex())

    def validate_match(self, home, away, season):
        sql = """SELECT * FROM `match` WHERE `HomeClub` = "{}" AND `AwayClub` = "{}" AND `Season` = "{}";""".format(home, away, season)
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        if len(myresult) == 0:
            err = QMessageBox()
            err.setText("This match doesn't exist!")
            err.exec()
            # print(Fore.RED + "This match doesn't exist!")
            # print(Fore.WHITE)
            return False
        return True

    def logged_out_state(self):
        # Changing welcom message
        welcome = "Welcome!"
        self.welcome_label.setText(welcome)

        # Changing logout status
        logout_txt = "You are not logged in!"
        self.logout_label.setText(logout_txt)
        self.logout_button.setEnabled(False)

        # Stopping reviews
        self.review_submit_button.setEnabled(False)

        # Removing credentials and allowing loggin in
        self.signin_email.setText("")
        self.signin_pw.setText("")
        self.signin_label.setText("")
        self.login_submit.setEnabled(True)


    def logged_in_state(self):
        # Changing welcom message
        welcome = "Welcome {}!".format(self.username)
        self.welcome_label.setText(welcome)

        # Changing logout status
        logout_txt = "You are logged in as {}.".format(self.username)
        self.logout_label.setText(logout_txt)
        self.logout_button.setEnabled(True)

        # Allowing match review
        self.review_submit_button.setEnabled(True)

        # Stopping logging in
        self.login_submit.setEnabled(False)

def main():
    app = QApplication(sys.argv)
    session_inst = session()
    session_inst.show()
    try:
        with open("style.qss", "r") as f:
            _style = f.read()
            app.setStyleSheet(_style)
    except:
        pass
    sys.exit(app.exec())
	
if __name__ == '__main__':
    main()