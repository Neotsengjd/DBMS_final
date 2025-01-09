# DBMS Final-Book Management System

# 專案說明

This project ...

Key Features:

1:Book Collection Management: Add, update, and delete books from your personal collection. The system allows detailed information for each book, including title, author, publication year, and genre.

2:Reading History: Track the books you have read, along with dates and personal notes. This feature helps users maintain a log of their reading journey.

3:Reading Plans: Create and manage reading plans to organize future reading schedules. Users can set goals and timelines for reading specific books.

4:Author Information Management: Update author details, including name, biography, nationality, and birth year, ensuring that the author database is always current.

5:PDF Upload and Reading: Upload and store PDF versions of books within the system. Users can also read these PDFs directly through an integrated PDF viewer, enhancing the reading experience.

# **Database Schema**

The database contains the following tables:

### Book

- **`id`**: Integer, Primary Key
- **`ISBN`**: Integer
- **`book_title`**: Text, Not Null
- **`author_id`**: Number
- **`author`**: Text
- **`price`**: Integer, Check (price >= 0)
- **`category`**: Text
- **`edition`**: Integer, Check (edition > 0)
- **`current_page`**: Integer, Check (current_page >= 0)
- **`pdf_path`**: Text

### ReadingHistory

- **`id`**: Integer, Primary Key
- **`time_stamp`**: Text
- **`book_id`**: Integer, Foreign Key (references Book(id)), Not Null
- **`bookpage`**: Integer, Check (bookpage >= 0)
- **`note`**: Text, Not Null

### ReadingPlan

- **`id`**: Integer, Primary Key
- **`book_id`**: Integer, Foreign Key (references Book(id)), Not Null
- **`expired_date`**: Text
- **`is_complete`**: Integer, Check (is_complete IN (0, 1))

### Note

- **`id`**: Integer, Primary Key
- **`book_id`**: Integer, Foreign Key (references Book(id)), Not Null
- **`title`**: Text
- **`content`**: Text
- **`created_at`**: Text
- **`updated_at`**: Text

### FavoriteList

- **`id`**: Integer, Primary Key
- **`book_id`**: Integer, Foreign Key (references Book(id)), Not Null
- **`book_title`**: Text

### Author (New Table)

- **`author_id`**: Integer, Primary Key
- **`author_name`**: Text, Not Null
- **`introduction`**: Text
- **`nationality`**: Text
- **`Birth_year`**: Integer, Check (Birth_year > 0)


# **Backend Features**

### **Book Management**

- **Check Book**: Check if a book with the same title already exists.
- **Add Book**: Add a new book to the library. If a book with the same title exists, the user will be prompted to confirm adding a duplicate.
- **Upload PDF**: Upload a PDF file associated with a book. The file path is stored in the pdf_path column. 
- **View PDF**: View the uploaded PDF file of a book. 
- **Add Author**: Add a new author information.
