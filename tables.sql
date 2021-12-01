CREATE TABLE Winter_Game (year YEAR PRIMARY KEY, city VARCHAR(100));
CREATE TABLE Winter_Event (eventID INT PRIMARY KEY, discipline VARCHAR(100), event VARCHAR(100), sport VARCHAR(100));
CREATE TABLE Winter_Athlete (athleteID INT PRIMARY KEY, name VARCHAR(100), country CHAR(3), gender VARCHAR(5));
CREATE TABLE Winter_Medalists (athleteID INT, eventID INT, year YEAR, medal VARCHAR(6));
CREATE TABLE Summer_Game (year YEAR PRIMARY KEY, city VARCHAR(100));
CREATE TABLE Summer_Event (eventID INT PRIMARY KEY, discipline VARCHAR(100), event VARCHAR(100), sport VARCHAR(100));
CREATE TABLE Summer_Athlete (athleteID INT PRIMARY KEY, name VARCHAR(100), country CHAR(3), gender VARCHAR(5));
CREATE TABLE Summer_Medalists (athleteID INT, eventID INT, year YEAR, medal VARCHAR(6));