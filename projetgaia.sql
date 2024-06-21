CREATE TABLE `utilisateur` (
  `IdUtilisateur` int NOT NULL AUTO_INCREMENT,
  `Nom` varchar(100) NOT NULL,
  `Prenom` varchar(100) NOT NULL,
  `Age` int NOT NULL,
  `Adresse` tinytext NOT NULL,
  `NumClient` varchar(255) NOT NULL,
  PRIMARY KEY (`IdUtilisateur`)
);

INSERT INTO `utilisateur` (`IdUtilisateur`, `Nom`, `Prenom`, `Age`, `Adresse`, `NumClient`) VALUES 
(1, 'Dupont', 'Jean', 30, '1 Rue de Paris', '12345'),
(2, 'Martin', 'Paul', 35, '2 Rue de Lyon', '67890'),
(3, 'Durand', 'Pierre', 40, '3 Rue de Marseille', '54321'),
(4, 'Moreau', 'Jacques', 45, '4 Rue de Nice', '09876'),
(5, 'Petit', 'Louis', 50, '5 Rue de Toulouse', '11223');

CREATE TABLE `position` (
  `IdPosition` int NOT NULL AUTO_INCREMENT,
  `Latitude` float NOT NULL,
  `Longitude` float NOT NULL,
  `Altitude` float NOT NULL,
  `FKIdUtilisateur` int NOT NULL,
  PRIMARY KEY (`IdPosition`),
  KEY `FKIdUtilisateur` (`FKIdUtilisateur`),
  CONSTRAINT `position_ibfk_1` FOREIGN KEY (`FKIdUtilisateur`) REFERENCES `utilisateur` (`IdUtilisateur`)
);

INSERT INTO `position` (`IdPosition`, `Latitude`, `Longitude`, `Altitude`, `FKIdUtilisateur`) VALUES 
(1, -20.8821, 55.4507, 50.0, 1),
(2, -20.8822, 55.4508, 55.0, 2),
(3, -20.8823, 55.4509, 60.0, 3),
(4, -20.8824, 55.4510, 65.0, 4),
(5, -20.8825, 55.4511, 70.0, 5);

CREATE TABLE `donnees` (
  `IdDonnees` int NOT NULL AUTO_INCREMENT,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `DCE` float NOT NULL,
  `TCEAM` float NOT NULL,
  `TCEAMB` int NOT NULL,
  `TCEAV` int NOT NULL,
  `ENS` float NOT NULL,
  `EEC` float NOT NULL,
  `FKIdPosition` int NOT NULL,
  PRIMARY KEY (`IdDonnees`),
  KEY `FKIdPosition` (`FKIdPosition`),
  CONSTRAINT `donnees_ibfk_1` FOREIGN KEY (`FKIdPosition`) REFERENCES `position` (`IdPosition`)
);

INSERT INTO `donnees` (`IdDonnees`, `Timestamp`, `DCE`, `TCEAM`, `TCEAMB`, `TCEAV`, `ENS`, `EEC`, `FKIdPosition`) VALUES 
(1, '2024-03-13 09:48:57', 1.5, 24.0, 30, 26, 100.0, 2.0, 1),
(2, '2024-03-13 09:49:10', 1.4, 20.0, 22, 24, 80.0, 1.5, 2),
(3, '2024-03-13 09:49:45', 2.0, 10.0, 29, 24, 120.0, 3.0, 1),
(5, '2024-03-13 09:50:04', 2.5, 15.0, 26, 25, 40.0, 1.0, 2),
(6, '2024-03-13 09:50:31', 3.5, 9.0, 20, 26, 3.1, 3.0, 5),
(8, '2024-12-17 12:15:47', 2.1, 15.0, 14, 27, 62.0, 0.4, 5),
(9, '2023-07-06 15:59:02', 3.3, 6.0, 21, 24, 44.0, 0.2, 1),
(10, '2023-05-14 01:41:40', 4.0, 9.0, 22, 24, 10.0, 3.2, 5),
(11, '2024-09-04 15:40:53', 2.4, 9.0, 28, 28, 82.0, 4.1, 1),
(12, '2024-09-27 08:40:28', 1.6, 7.0, 11, 16, 3.0, 4.9, 4),
(13, '2023-03-09 08:47:25', 1.2, 30.0, 26, 29, 48.0, 0.8, 3),
(14, '2024-02-17 23:03:13', 5.0, 11.0, 16, 27, 115.0, 2.3, 3),
(15, '2024-07-19 15:18:32', 3.3, 19.0, 10, 22, 32.0, 4.6, 4),
(16, '2023-10-01 00:56:57', 2.5, 24.0, 25, 20, 50.0, 0.6, 2),
(17, '2023-09-22 18:23:56', 4.1, 26.0, 25, 20, 54.0, 1.1, 4),
(18, '2024-10-26 12:35:28', 2.7, 14.0, 21, 25, 73.0, 0.4, 3),
(19, '2024-04-14 06:19:56', 2.9, 17.0, 11, 25, 44.0, 3.8, 4),
(20, '2023-05-04 03:13:23', 4.1, 14.0, 19, 19, 8.0, 2.1, 5),
(21, '2023-11-21 12:00:44', 2.5, 20.0, 26, 17, 51.0, 3.2, 5);
