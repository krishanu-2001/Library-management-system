# ddl statements
# 16 tables

drop database library;
create database library;
use library;
CREATE TABLE librarian(
	librarian_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(100),
    address VARCHAR(100),
    password VARCHAR(100),
    notes VARCHAR(100),
    PRIMARY KEY (librarian_id)
);
CREATE TABLE user (
    user_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
	role VARCHAR(100),
    password VARCHAR(100),
    unpaid_fines decimal(6,2) DEFAULT 0.00,
    address VARCHAR(100),
    notes VARCHAR(100),
    PRIMARY KEY (user_id)
);
CREATE TABLE books(
	isbn VARCHAR(100) UNIQUE not null,
    author VARCHAR(100),
    title VARCHAR(100),
    rating DECIMAL(4,2) DEFAULT 0,
	current_status VARCHAR(100) DEFAULT 'on-shelf',
	copy_number INT,
	year_of_publication INT,
    shelf_id VARCHAR(100),
    notes VARCHAR(100),
    user_id VARCHAR(100),
    due_date DATE,
    issue_email_date DATE,
    issue_date DATE,
    issue_status VARCHAR(100),
-- 	CONSTRAINT `check_date` CHECK (`issue_date` = NULL or `issue_email_date`= NULL or DATEDIFF(`due_date`, CURDATE()) < 0 and DATEDIFF(CURDATE(), `issue_email_date`) < 15),
    PRIMARY KEY (isbn, copy_number),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE shelf (
    shelf_id VARCHAR(100) UNIQUE NOT NULL,
    capacity INT,
    notes VARCHAR(100),
    PRIMARY KEY (shelf_id)
);

CREATE TABLE genre (
	genre_id VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    notes VARCHAR(100),
    PRIMARY KEY (genre_id)
);

CREATE TABLE reading_list (
    user_id VARCHAR(100),
    name VARCHAR(100) NOT NULL,
    list_url VARCHAR(100) NOT NULL,
    type VARCHAR(45) NOT NULL,
    PRIMARY KEY (list_url),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE personal_book_shelf (
    user_id VARCHAR(100) NOT NULL,
    shelf_name VARCHAR(100) NOT NULL,
    shelf_url VARCHAR(100) NOT NULL,
    PRIMARY KEY (shelf_url),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);
## relations below

CREATE TABLE keeps_track (
	librarian_id VARCHAR(100) NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    PRIMARY KEY (librarian_id, user_id),
    FOREIGN KEY (librarian_id) REFERENCES librarian(librarian_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE maintain (
	librarian_id VARCHAR(100) NOT NULL,
    isbn VARCHAR(100) NOT NULL,
    PRIMARY KEY (librarian_id, isbn),
    FOREIGN KEY (librarian_id) REFERENCES librarian(librarian_id),
    FOREIGN KEY (isbn) REFERENCES books(isbn) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE belongs_to (
	genre_id VARCHAR(100) NOT NULL,
    isbn VARCHAR(100) NOT NULL,
    PRIMARY KEY (genre_id, isbn),
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id),
    FOREIGN KEY (isbn) REFERENCES books(isbn) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE favourite (
	genre_id VARCHAR(100) NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    PRIMARY KEY (genre_id, user_id),
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE hold (
	isbn VARCHAR(100) NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    hold_date DATE,
    hold_email_date DATE,
    hold_status VARCHAR (200) DEFAULT "PENDING",
    PRIMARY KEY (isbn, user_id),
    FOREIGN KEY (isbn) REFERENCES books(isbn) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user(user_id) 
);

CREATE TABLE return_books (
	isbn VARCHAR(100) NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    return_date DATE,
    issue_date DATE,
    return_status VARCHAR(100),
    fine DECIMAL(6,2),
    fine_paid TINYINT DEFAULT 0,
    PRIMARY KEY (isbn, user_id),
    FOREIGN KEY (isbn) REFERENCES books(isbn) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE rate (
	isbn VARCHAR(100) NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    rating DECIMAL(4,2) DEFAULT 0,
    review VARCHAR(200),
    PRIMARY KEY (isbn, user_id),
    FOREIGN KEY (isbn) REFERENCES books(isbn) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE friend (
	user_id VARCHAR(100) NOT NULL,
    friend_id VARCHAR(100) NOT NULL,
    status TINYINT NOT NULL,
    PRIMARY KEY (friend_id, user_id),
    FOREIGN KEY (friend_id) REFERENCES user(user_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE reading_list_contains (
    list_url VARCHAR(100) NOT NULL,
    isbn VARCHAR(100) NOT NULL,
    PRIMARY KEY (list_url,isbn),
    FOREIGN KEY (isbn) REFERENCES books(isbn) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (list_url) REFERENCES reading_list(list_url) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE follow (
    list_url VARCHAR(100) NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    PRIMARY KEY (list_url,user_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (list_url) REFERENCES reading_list(list_url) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE personal_book_shelf_contains (
	isbn VARCHAR(100) NOT NULL,
    shelf_url VARCHAR(100) NOT NULL,
    PRIMARY KEY (shelf_url, isbn),
    FOREIGN KEY (isbn) REFERENCES books(isbn) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (shelf_url) REFERENCES personal_book_shelf(shelf_url) ON DELETE CASCADE ON UPDATE CASCADE
);
## 16 tables total 5 entity, 11 relations



