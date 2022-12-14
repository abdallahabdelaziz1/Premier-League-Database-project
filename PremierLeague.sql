CREATE SCHEMA IF NOT EXISTS `premierleague`;

CREATE TABLE IF NOT EXISTS Player (
	PlayerName VARCHAR(40) NOT NULL,
    BirthDate DATE NOT NULL,
    Weight INT,
    Height INT,
    `Position` VARCHAR(20) NOT NULL,
    Nationality VARCHAR(20) NOT NULL,
    PRIMARY KEY(PlayerName, BirthDate)
);

CREATE TABLE IF NOT EXISTS Stadium (
	StadiumName VARCHAR(50) NOT NULL PRIMARY KEY,
    RecordAttendence INT,
    DateBuiling INT NOT NULL,
    Capacity INT NOT NULL,
    PitchWidth FLOAT,
    PitchLength FLOAT,
    AddressCity VARCHAR(20),
    AddressPC VARCHAR(10),
    AddressArea VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Club (
	ClubName VARCHAR(30) NOT NULL PRIMARY KEY,
    Website VARCHAR(70) NOT NULL,
    ClubStadium VARCHAR(50) NOT NULL,
    CONSTRAINT FK_Owns FOREIGN KEY Club(ClubStadium) REFERENCES Stadium(StadiumName)
    ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS PlaysFor (
	PlayerName VARCHAR(40) NOT NULL,
    BirthDate DATE NOT NULL,
    ClubName VARCHAR(30) NOT NULL,
    Season CHAR(7) NOT NULL,
    PRIMARY KEY(PlayerName, BirthDate, ClubName, Season),
    CONSTRAINT FK_PlaysForPlayer FOREIGN KEY PlaysFor(PlayerName, BirthDate) REFERENCES Player(PlayerName, BirthDate)
	ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT FK_PlaysForClub FOREIGN KEY PlaysFor(ClubName) REFERENCES Club(ClubName)
	ON UPDATE CASCADE ON DELETE RESTRICT
);



CREATE TABLE IF NOT EXISTS `Match` (
    HomeClub VARCHAR(30) NOT NULL,
    AwayClub VARCHAR(30) NOT NULL,
    Season CHAR(7) NOT NULL,
    MatchDate Date NOT NULL,
    HomeFouls INT NOT NULL,
    HomeGoals INT NOT NULL,
    HomeYellow INT NOT NULL,
    HomeRed INT NOT NULL,
    HomeShots INT NOT NULL,
    HomePossession DECIMAL(4,2) NOT NULL,
    AwayFouls INT NOT NULL,
    AwayGoals INT NOT NULL,
    AwayYellow INT NOT NULL,
    AwayRed INT NOT NULL,
    AwayShots INT NOT NULL,
    AwayPossession DECIMAL(4,2) NOT NULL,
    StadiumName VARCHAR(50) NOT NULL,
    PRIMARY KEY(HomeClub, AwayClub, Season),
    CONSTRAINT FK_MatchHome FOREIGN KEY `Match`(HomeClub) REFERENCES Club(ClubName)
    ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT FK_MatchAway FOREIGN KEY `Match`(AwayClub) REFERENCES Club(ClubName)
    ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT FK_Playedin FOREIGN KEY `Match`(StadiumName) REFERENCES Stadium(StadiumName)
    ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Fan (
	Email VARCHAR(100) NOT NULL PRIMARY KEY,
    `Password` CHAR(32) NOT NULL,
    UserName VARCHAR(20) NOT NULL,
    Gender CHAR NOT NULL,
    FavClub VARCHAR(30) NOT NULL,
    BirthDate DATE NOT NULL,
    CONSTRAINT FK_Favorite FOREIGN KEY Fan(FavClub) REFERENCES Club(ClubName)
    ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS MatchReview (
	FanEmail VARCHAR(100) NOT NULL,
    HomeClub VARCHAR(30) NOT NULL,
    AwayClub VARCHAR(30) NOT NULL,
    Season CHAR(7) NOT NULL,
    Rating INT NOT NULL,
    ReviewText VARCHAR(1000) NOT NULL,
    CONSTRAINT Rating_Check CHECK(Rating BETWEEN 1 AND 10),
    PRIMARY KEY(FanEmail, HomeClub, AwayClub, Season),
    CONSTRAINT FK_MatchReviwed FOREIGN KEY MatchReview(HomeClub, AwayClub, Season) REFERENCES `Match`(HomeClub, AwayClub, Season)
    ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT FK_Reviews FOREIGN KEY MatchReview(FanEmail) REFERENCES Fan(Email)
    ON UPDATE CASCADE ON DELETE CASCADE
);


