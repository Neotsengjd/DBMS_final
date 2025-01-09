# DBMS Final:　Meal Management System

# 專案說明

This project ...

Key Features:

1: Management: Add, update, and delete books from your personal collection. The system allows detailed information for each book, including title, author, publication year, and genre.

2:Reading History: Track the books you have read, along with dates and personal notes. This feature helps users maintain a log of their reading journey.

3:Reading Plans: Create and manage reading plans to organize future reading schedules. Users can set goals and timelines for reading specific books.

4:Author Information Management: Update author details, including name, biography, nationality, and birth year, ensuring that the author database is always current.

5:PDF Upload and Reading: Upload and store PDF versions of books within the system. Users can also read these PDFs directly through an integrated PDF viewer, enhancing the reading experience.

# **Database Schema**

The database contains the following tables:

### FOOD

- **`FoodID`**: Integer, Primary Key
- **`Fat`**: float
- **`Protein`**: float
- **`Starch`**: float
- **`Calories`**: float
- **`FName`**: Text

### USERS

- **`ID`**: Integer, Not Null, Primary Key
- **`UName`**: Text, Not Null
- **`Gender`**: Text(M, F)
- **`Age`**: Integer, Check (Age >= 0)
- **`Height`**: float
- **`Weight`**: float
- **`Account`**: Text
- **`Password`**: int
- **`Activity_level`**: int


### USER_GOAL

- **`U_GoalID`**: Integer, Primary Key
- **`UID`**: Integer, Foreign Key (references USERS(ID)), Not Null
- **`Fat`**: float
- **`Protein`**: float
- **`Starch`**: float
- **`S_DATE`**: date
- **`E_DATE`**: date

### MEAL 

- **`MealID`**: Integer, Primary Key
- **`UID`**: Integer, Primary Key, Foreign Key (references USERS(ID))
- **`Dates`**: date
- **`Times`**: Time
- **`Category`**: Text

### MEAL_FOOD

- **`FoodID`**: Integer, Primary Key, Foreign Key (references FOOD (FoodID))
- **`MealID`**: Integer, Primary Key, Foreign Key (references MEAL (UID, MealID))
- **`UID`**: Integer, Primary Key, Foreign Key (references MEAL (UID, MealID))
- **`Count`**: Integer

### GROUP_LEADER

- **`GroupID`**: Integer, Primary Key
- **`Leader`**: Integer, Primary Key, Foreign Key (references USERS(ID))
- **`GName`**: Text

### GROUP_MEMBER

- **`M_GroupID`**: Integer, Primary Key, Foreign Key (references GROUP_LEADER(Group_ID))
- **`Members`**: Integer, Primary Key, Foreign Key (references USERS(ID))


# **Backend Features**

### **Management**

- **Check User's Information**: Check if a user already exists or update it.
- **Add Meal**: Add a new meal to the databases.
- **Join Group**: Join a new group to cheeck the member. 
- **Set goal**: Someone can set their goal and check the goal in joined groups.
