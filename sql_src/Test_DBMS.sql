USE DBMS;
-- Insert Users
INSERT INTO Users (UName, UPassword, UAccount, NoticeTime)
VALUES ('Mason', 'password', 'mason_account', 20021227);
INSERT INTO Users (UName, UPassword, UAccount, NoticeTime)
VALUES ('Jeffery', 'password', 'jeffery_account', 20011108);
INSERT INTO Users (UName, UPassword, UAccount, NoticeTime)
VALUES ('Eden', 'password', 'Eden_account', 20021027);
INSERT INTO Users (UName, UPassword, UAccount, NoticeTime)
VALUES ('David', 'password', 'David_account', 20030712);

-- Insert ledgers
INSERT INTO Ledgers (UID, LName)
VALUES (1, 'mason_ledger_1');
INSERT INTO Ledgers (UID, LName)
VALUES (1, 'mason_ledger_2');
INSERT INTO Ledgers (UID, LName)
VALUES (2, 'jeffery_ledger_1');
INSERT INTO Ledgers (UID, LName)
VALUES (2, 'jeffery_ledger_2');
INSERT INTO Ledgers (UID, LName)
VALUES (3, 'eden_ledger_1');
INSERT INTO Ledgers (UID, LName)
VALUES (3, 'eden_ledger_2');
INSERT INTO Ledgers (UID, LName)
VALUES (4, 'david_ledger_1');
INSERT INTO Ledgers (UID, LName)
VALUES (4, 'david_ledger_2');

-- Insert datas
INSERT INTO Datas (UID, LName, Price, DName, DType, DDate)
VALUES (1, 'mason_ledger_1', 150, 'breakfast', 'food', '20240430');
INSERT INTO Datas (UID, LName, Price, DName, DType, DDate)
VALUES (1, 'mason_ledger_1', 200, 'lunch', 'food', '20240430');
INSERT INTO Datas (UID, LName, Price, DName, DType, DDate)
VALUES (1, 'mason_ledger_2', 55000, 'computer', 'education', '20240429');
INSERT INTO Datas (UID, LName, Price, DName, DType, DDate)
VALUES (1, 'mason_ledger_2', 600, 'book', 'education', '20240429');

INSERT INTO Datas (UID, LName, Price, DName, DType, DDate)
VALUES (2, 'jeffery_ledger_1', 125, 'brunch', 'food', '20240428');
INSERT INTO Datas (UID, LName, Price, DName, DType, DDate)
VALUES (2, 'jeffery_ledger_1', 375, 'dinner', 'food', '20240416');
INSERT INTO Datas (UID, LName, Price, DName, DType, DDate)
VALUES (2, 'jeffery_ledger_2', 1500, 'text_book', 'education', '20240429');
INSERT INTO Datas (UID, LName, Price, DName, DType, DDate)
VALUES (2, 'jeffery_ledger_2', 1000, 'A_Yi', 'relationship', '20240429');

INSERT INTO Datas (UID, LName, Price, DName, DType, DDate)
VALUES (3, 'eden_ledger_1', 125, 'morning_food', 'food', '20240428');
INSERT INTO Datas (UID, LName, Price, DName, DType, DDate)
VALUES (3, 'eden_ledger_1', 375, 'night_food', 'food', '20240416');
INSERT INTO Datas (UID, LName, Price, DName, DType, DDate)
VALUES (3, 'eden_ledger_2', 30000, 'Tainan', 'trip', '20240429');
INSERT INTO Datas (UID, LName, Price, DName, DType, DDate)
VALUES (3, 'eden_ledger_2', 1000, 'A_dai', 'relationship', '20240429');

INSERT INTO Datas (UID, LName, Price, DName, DType, DDate)
VALUES (4, 'david_ledger_1', 20, 'MRT', 'traffic', '20240428');
INSERT INTO Datas (UID, LName, Price, DName, DType, DDate)
VALUES (4, 'david_ledger_1', 899, 'shian_shi_tian_tang', 'food', '20240416');
INSERT INTO Datas (UID, LName, Price, DName, DType, DDate)
VALUES (4, 'david_ledger_2', 1200, 'Kaoshung', 'trip', '20240429');
INSERT INTO Datas (UID, LName, Price, DName, DType, DDate)
VALUES (4, 'david_ledger_2', 90, 'drink', 'food', '20240429');
