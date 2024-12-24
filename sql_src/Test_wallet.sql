
-- Insert some data
INSERT INTO Users (UName, UPassword, UAccount) VALUES ('a', 'a', 'a'); -- uid = 1
INSERT INTO Users (UName, UPassword, UAccount) VALUES ('b', 'b', 'b'); -- uid = 2
INSERT INTO Users (UName, UPassword, UAccount) VALUES ('c', 'c', 'c'); -- uid = 3

INSERT INTO Wallets (UID, WName) VALUES (1, 'Wallet1'); -- wid = 1
INSERT INTO Wallets (UID, WName) VALUES (1, 'Wallet2'); -- wid = 2
INSERT INTO Wallets (UID, WName) VALUES (2, 'Wallet3'); -- wid = 3
Insert INTO Wallets (UID, WName) VALUES (3, 'Wallet4'); -- wid = 4

INSERT INTO Ledgers (WID, LName) VALUES (1, 'Ledger1'); -- lid = 1
INSERT INTO Ledgers (WID, LName) VALUES (1, 'Ledger2'); -- lid = 2
INSERT INTO Ledgers (WID, LName) VALUES (2, 'Ledger3'); -- lid = 3
Insert INTO Ledgers (WID, LName) VALUES (3, 'Ledger4'); -- lid = 4

INSERT INTO Goals (UID, GName, GTargetAmount, GCurrentAmount, GDate) VALUES (1, 'Goal1', 100, 300, '2021-12-31'); -- gid = 1
INSERT INTO Goals (UID, GName, GTargetAmount, GCurrentAmount, GDate) VALUES (1, 'Goal2', 200, 400, '2021-12-31'); -- gid = 2
INSERT INTO Goals (UID, GName, GTargetAmount, GCurrentAmount, GDate) VALUES (2, 'Goal3', 300, 0, '2021-12-31'); -- gid = 3
Insert INTO Goals (UID, GName, GTargetAmount, GCurrentAmount, GDate) VALUES (3, 'Goal4', 400, 0, '2021-12-31'); -- gid = 4

INSERT INTO Datas (UID, LName, Price, DName, DType, DDate) VALUES (1, 'Ledger1', 100, 'Data1', 'Income', '2021-12-31'); -- did = 1
INSERT INTO Datas (UID, LName, Price, DName, DType, DDate) VALUES (1, 'Ledger1', 200, 'Data2', 'Income', '2021-12-31'); -- did = 2
INSERT INTO Datas (UID, LName, Price, DName, DType, DDate) VALUES (2, 'Ledger3', 400, 'Data3', 'Income', '2021-12-31'); -- did = 3

INSERT INTO DataToGoal (DID, GID) VALUES (1, 1);
INSERT INTO DataToGoal (DID, GID) VALUES (2, 1);
INSERT INTO DataToGoal (DID, GID) VALUES (3, 2);

INSERT INTO DataToLedger (DID, LID) VALUES (1, 1);
INSERT INTO DataToLedger (DID, LID) VALUES (2, 1);
INSERT INTO DataToLedger (DID, LID) VALUES (3, 3);