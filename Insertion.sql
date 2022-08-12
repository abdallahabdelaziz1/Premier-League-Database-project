LOAD DATA INFILE 'E:/AUC/Courses/_now/CSCE_2501 Fundmntals of Database Systems/Project/Phase 2/Data/StadiumTable2.csv'
INTO TABLE stadium
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(StadiumName, @vRecordAttendence, DateBuiling, Capacity, @vPitchWidth, @vPitchLength, @vAddressCity, @vAddressPC, @vAddressArea)
SET
RecordAttendence = NULLIF(@vRecordAttendence,''),
PitchWidth = NULLIF(@PitchWidth,''),
PitchLength = NULLIF(@vPitchLength,''),
AddressCity = NULLIF(@vAddressCity,''),
AddressPC = NULLIF(@vAddressPC,''),
AddressArea = NULLIF(@vAddressArea,'');

LOAD DATA INFILE 'E:/AUC/Courses/_now/CSCE_2501 Fundmntals of Database Systems/Project/Phase 2/Data/ClubTable.csv'
INTO TABLE club
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'E:/AUC/Courses/_now/CSCE_2501 Fundmntals of Database Systems/Project/Phase 2/Data/PlayerTable.csv'
INTO TABLE player
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(PlayerName, BirthDate, @vWeight, @vHeight, `Position`, Nationality)
SET
Weight = NULLIF(@vWeight,''),
Height = NULLIF(@vHeight,'');

LOAD DATA INFILE 'E:/AUC/Courses/_now/CSCE_2501 Fundmntals of Database Systems/Project/Phase 2/Data/PlaysForTable.csv'
INTO TABLE playsfor
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'E:/AUC/Courses/_now/CSCE_2501 Fundmntals of Database Systems/Project/Phase 2/Data/MatchTable.csv'
INTO TABLE `match`
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

INSERT INTO fan
VALUES ("abdallah_taha@aucegypt.edu", "AUC Pass", "Abdallah123", "M", "Liverpool", "1979-2-22"),
("alo@aucegypt.edu", "CSCE AUC", "Alo123", "M", "Chelsea", "2000-5-15");

INSERT INTO matchreview
VALUES ("abdallah_taha@aucegypt.edu", "Leicester City","Brentford","2021/22", 8, "Good Game!"), 
("alo@aucegypt.edu", "Chelsea", "Liverpool", "2021/22", 9, "Great Game!");
