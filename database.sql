CREATE DATABASE Vivai;

CREATE TABLE Vivai.SupportedPlant(
   id INT PRIMARY KEY AUTO_INCREMENT,
   species VARCHAR(100) NOT NULL,
   websiteUrl VARCHAR(1000) NOT NULL
 );

CREATE TABLE Vivai.Plant(
  id INT PRIMARY KEY AUTO_INCREMENT,
  species VARCHAR(100) NOT NULL,
  family VARCHAR(100),
  picUrl VARCHAR(1000) NOT NULL,
  waterNeed Enum("faible","moyen","important") NOT NULL,
  careLevel Enum("facile","modéré","difficile") NOT NULL,
  growth Enum("janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre") NOT NULL,
  coldResistance Enum("fragile","à protéger","résistante") NOT NULL,
  sunNeed Enum("ombre","mi-ombre","soleil") NOT NULL,
  heightMature INT NOT NULL,
  widthMature INT NOT NULL
);

CREATE TABLE Vivai.UserPlant(
  id INT PRIMARY KEY AUTO_INCREMENT,
  plantId INT NOT NULL,
  userId VARCHAR(100) NOT NULL,
  nickname VARCHAR(100),
  location VARCHAR(100),
  temperature VARCHAR(100),
  sunExpo Enum("1", "2", "3"),
  shared BOOLEAN DEFAULT FALSE,
  CONSTRAINT fk_userplant_plantid FOREIGN KEY(plantId) REFERENCES Vivai.Plant(id)
);

CREATE TABLE Vivai.Reporting(
  userPlantId INT NOT NULL,
  reportDate DATE NOT NULL,
  water BOOLEAN DEFAULT FALSE,
  prune BOOLEAN DEFAULT FALSE,
  repotting BOOLEAN DEFAULT FALSE,
  harvest BOOLEAN DEFAULT FALSE,
  state Enum("bad", "medium", "good"),
  CONSTRAINT pk_reporting_userplantid_reportdate PRIMARY KEY(userPlantId, reportDate),
  CONSTRAINT fk_reporting_userplantid FOREIGN KEY(userPlantId) REFERENCES Vivai.UserPlant(id)
);

