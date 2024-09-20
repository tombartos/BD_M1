--Creation des domaines pour l'etat des livres et le status des emprunts

CREATE DOMAIN typeEtat
AS VARCHAR(20) 
CHECK(VALUE IN('bon','degrade','perdu'));

CREATE DOMAIN typeEmp
AS VARCHAR(20) 
CHECK(VALUE IN('rendu','non rendu'));

--Creation des tables

CREATE TABLE Auteurs
(
  IDAuteur SERIAL PRIMARY KEY,
  NomAut VARCHAR(20),
  PrenomAut VARCHAR(20),
  NaissanceAut DATE,
  Mort DATE,
  Nationalite VARCHAR(15)
  );

CREATE TABLE Editeurs
(
  NomEdit VARCHAR(20) PRIMARY KEY,
  Patron VARCHAR(40),
  Pays VARCHAR(15)
  );

CREATE TABLE Livres
(
  ISBN VARCHAR(20) PRIMARY KEY,
  Titre VARCHAR(50),
  IDAuteur INT REFERENCES Auteurs,
  NomEdit VARCHAR(20) REFERENCES Editeurs,
  DateSortie DATE,
  Genre VARCHAR(20),
  QteDispo INTEGER DEFAULT 1,
  PrixAchat FLOAT NOT NULL
  );

CREATE TABLE Clients
(
  IDClient SERIAL PRIMARY KEY,
  NomCl VARCHAR(20),
  PrenomCl VARCHAR(20),
  NaissanceCl DATE
);

CREATE TABLE Emprunt
(
  NoEmp SERIAL PRIMARY KEY,
  ISBN VARCHAR(20) REFERENCES Livres,
  IDClient INT REFERENCES Clients,
  DateDeb DATE NOT NULL,
  DateFin DATE NOT NULL,
  QteEmp INTEGER NOT NULL DEFAULT 1,
  StatusEmp typeEmp,
  StatusLivre typeEtat,
  
  CONSTRAINT dates
  CHECK (DateDeb < DateFin)
);

CREATE TABLE Achat
(
  NoAchat SERIAL PRIMARY KEY,
  ISBN VARCHAR(20) REFERENCES Livres,
  IDClient INT REFERENCES Clients,
  DateAchat DATE,
  QteAchat INTEGER NOT NULL DEFAULT 1,
  PrixTotAchat FLOAT DEFAULT 0
);

--Creation du trigger sur Achat qui gere le calcul du prix total d'un achat, le retrait de la quantite en stock
--Lors d'un achat ainsi que le reaprovisionnement automatique en cas de rupture et verifie que l'on ai assez de stock
--Pour satisfaire l'achat
CREATE OR REPLACE FUNCTION Fachat()
RETURNS trigger AS
    $$
        DECLARE prix FLOAT;
        DECLARE isbntmp VARCHAR(20);
        DECLARE noachattmp INT;
        DECLARE qteStock INT;
        DECLARE qteAchete INT;
        BEGIN

              SELECT max(NoAchat) FROM Achat --On recupere le numero de l'achat
              INTO noachattmp;

              SELECT ISBN FROM Achat  --On recupere l'ISBN du dernier livre achete (on suppose que c'est le NoAchat le plus eleve)
              WHERE NoAchat = noachattmp
              INTO isbntmp;

              SELECT PrixAchat From Achat, Livres   --On recupere le prix du livre a l'unite
              WHERE Livres.ISBN = isbntmp
              INTO prix;

              SELECT qtedispo FROM Livres WHERE ISBN = isbntmp   --On recupere la quantite dispo en stock
              INTO qteStock;

              SELECT QteAchat FROM Achat WHERE NoAchat = noachattmp  --On recupere la quantite qu'on veut acheter
              INTO qteAchete;

              IF qteStock > qteAchete THEN      --Si on a assez de stock on les vends
                UPDATE Livres                         
                SET qtedispo = qtedispo - qteAchete
                WHERE ISBN = isbntmp;
                
              ELSIF qteStock = qteAchete THEN   --Si on en a pile le nombre que le client veut acheter on vend et on restock
                UPDATE Livres                    
                SET qtedispo = 5 
                WHERE ISBN = isbntmp;
                RAISE NOTICE 'Dernier livre vendu, restockage automatique';
              
              ELSE             --On a pas assez de stock pour satisfaire l'achat, on annule l'achat
                DELETE FROM Achat WHERE NoAchat = noachattmp;
                RAISE NOTICE 'Pas assez de stock pour satisfaire l achat, abandon';
                RETURN NULL;          --On return ici pour ne pas mettre a jour le prix total en cas d'abandon de l'achat

              END IF;
            
              UPDATE Achat      --On met a jour le prix total de l'achat
              SET PrixTotAchat = QteAchat * prix
              WHERE NoAchat = noachattmp;

        RETURN NULL;
        END;
    $$ LANGUAGE 'plpgsql';

CREATE OR REPLACE TRIGGER Tachat
AFTER INSERT ON Achat FOR EACH ROW
EXECUTE PROCEDURE Fachat();


--Creation du trigger sur Emprunt qui vérifie le stock avec de permettre l'emprunt et qui met le stock à jour après.
CREATE OR REPLACE FUNCTION Femprunt()
RETURNS trigger AS
    $$
        DECLARE isbntmp VARCHAR(20);
        DECLARE noemprunttmp INT;
        DECLARE qteStock INT;
        DECLARE qteEmprunt INT;
        BEGIN

              SELECT max(NoEmp) FROM Emprunt --On recupere le numero de l'emprunt
              INTO noemprunttmp;

              SELECT ISBN FROM Emprunt  --On recupere l'ISBN du dernier livre emprunté (on suppose que c'est le NoEmp le plus eleve)
              WHERE NoEmp = noemprunttmp
              INTO isbntmp;

              SELECT qtedispo FROM Livres WHERE ISBN = isbntmp   --On recupere la quantite dispo en stock
              INTO qteStock;

              SELECT QteEmp FROM Emprunt WHERE NoEmp = noemprunttmp  --On recupere la quantite qu'on veut emprunter
              INTO qteEmprunt;

              IF qteStock >= qteEmprunt THEN      --Si on a assez de stock on permet l'emprunt
                UPDATE Livres                         
                SET qtedispo = qtedispo - qteEmprunt
                WHERE ISBN = isbntmp;
                IF qteStock = qteEmprunt THEN
                  RAISE NOTICE 'Dernier livre emprunte, momentanement indisponible';
                END IF;
              
              ELSE             --On a pas assez de stock pour satisfaire l'emprunt, on annule l'emprunt
                DELETE FROM Emprunt WHERE NoEmp = noemprunttmp;
                RAISE NOTICE 'Pas assez de stock pour satisfaire l emprunt, abandon';
              
              END IF;

        RETURN NULL;
        END;
    $$ LANGUAGE 'plpgsql';

CREATE OR REPLACE TRIGGER Temprunt
AFTER INSERT ON Emprunt FOR EACH ROW
EXECUTE PROCEDURE Femprunt();

--Remplissage des tables

INSERT INTO Auteurs (NomAut, PrenomAut, NaissanceAut, Mort, Nationalite)
VALUES ('Verne', 'Jules', '08/02/1828', '24/03/1905', 'France');
INSERT INTO Auteurs (NomAut, PrenomAut, NaissanceAut, Mort, Nationalite)
VALUES ('Rowling', 'J.K.', '31/07/1965', NULL, 'Angleterre');
INSERT INTO Auteurs (NomAut, PrenomAut, NaissanceAut, Mort, Nationalite)
VALUES ('King','Stephen', '21/09/1947', NULL, 'Etats-Unis');
INSERT INTO Auteurs (NomAut, PrenomAut, NaissanceAut, Mort, Nationalite)
VALUES ('Hugo','Victor', '26/02/1802', '22/05/1885', 'France');

INSERT INTO Editeurs (NomEdit, Patron, Pays)
VALUES ('Le Livre de Poche', 'Audrey Petit', 'France');
INSERT INTO Editeurs (NomEdit, Patron, Pays)
VALUES ('Gallimard Jeunesse', 'Hedwige Veuve Pasquet', 'France');
INSERT INTO Editeurs (NomEdit, Patron, Pays)
VALUES ('Pocket', 'Julie Cartier', 'France');

INSERT INTO Livres (ISBN, Titre, IDAuteur, NomEdit, DateSortie, Genre, QteDispo, PrixAchat)
VALUES ('978-2253006329', 'Vingt mille lieues sous les mers',1, 'Le Livre de Poche', '20/06/1870', 'Science-Fiction', 8, 6.9);
INSERT INTO Livres (ISBN, Titre, IDAuteur, NomEdit, DateSortie, Genre, QteDispo, PrixAchat)
VALUES ('978-2075193993', 'Harry Potter et le Prisonnier dAzkaban',2, 'Gallimard Jeunesse', '08/07/1999', 'Fantasie', 17, 40);
INSERT INTO Livres (ISBN, Titre, IDAuteur, NomEdit, DateSortie, Genre, QteDispo, PrixAchat)
VALUES ('978-2253096764', 'Carrie',3, 'Le Livre de Poche', '05/04/1974', 'Horreur', 4, 8.7);
INSERT INTO Livres (ISBN, Titre, IDAuteur, NomEdit, DateSortie, Genre, QteDispo, PrixAchat)
VALUES ('978-2266296144', 'Les Miserables',4, 'Pocket', '01/01/1862', 'Roman', 13, 11.9);

INSERT INTO Clients (NomCl, PrenomCl, NaissanceCl)
VALUES ('Carpenter', 'Sabrina', '11/05/1999');
INSERT INTO Clients (NomCl, PrenomCl, NaissanceCl)
VALUES ('McConaughey', 'Matthew', '04/11/1969');
INSERT INTO Clients (NomCl, PrenomCl, NaissanceCl)
VALUES ('Eilish', 'Billie', '18/12/2001');
INSERT INTO Clients (NomCl, PrenomCl, NaissanceCl)
VALUES ('Strong', 'Mark', '05/08/1963');

INSERT INTO Achat (ISBN, IDClient, DateAchat, QteAchat)
VALUES('978-2253006329', 1, '11/09/2024', 1);
INSERT INTO Achat (ISBN, IDClient, DateAchat, QteAchat)
VALUES('978-2075193993', 2, '12/09/2024', 3);
INSERT INTO Achat (ISBN, IDClient, DateAchat, QteAchat)
VALUES('978-2253096764', 2, '14/09/2024', 1);

INSERT INTO Emprunt (ISBN, IDClient, DateDeb, DateFin, QteEmp, StatusEmp, StatusLivre)
VALUES('978-2075193993', 3, '09/09/2024', '15/09/2024', 1, 'non rendu', 'bon');

--Quelques requetes d'exemple

--On veut recuperer la nationalite de l'auteur du dernier livre qu'a achete McConaughey
SELECT Nationalite
FROM Achat, Livres, Auteurs, Clients
WHERE Livres.IDAuteur = Auteurs.IDAuteur
AND Achat.IDClient = Clients.IDClient
AND Livres.ISBN = Achat.ISBN
AND Achat.NoAchat=(SELECT max(NoAchat)
                  FROM Achat,Clients
                  WHERE Clients.NomCl='McConaughey'
                  AND Achat.IDClient=Clients.IDClient);

--Un client veut connaitre le prix du livre Carrie
SELECT PrixAchat
FROM Livres
WHERE Livres.Titre='Carrie';

--On veut changer le patron de l'éditeur Pocket
UPDATE Editeurs
SET Patron='Yann Roblin'
WHERE NomEdit='Pocket';

--On veut connaître la date du premier achat du client 2
SELECT DateAchat
FROM Achat
WHERE NoAchat=(SELECT min(NoAchat)
              FROM Achat
              WHERE Achat.IDClient=2);

--On veut la date de naissance de Carpenter
SELECT NaissanceCl
FROM Clients
WHERE NomCl='Carpenter';