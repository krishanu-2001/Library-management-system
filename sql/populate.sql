# sql statements

INSERT INTO librarian (librarian_id, name, address, password) VALUES ('1', 'emp1', 'alpha', '1234');
INSERT INTO librarian (librarian_id, name, address, password) VALUES ('2', 'emp2', 'beta', '1234');
INSERT INTO librarian (librarian_id, name, address, password) VALUES ('3', 'emp3', 'gamma', '1234');
INSERT INTO librarian (librarian_id, name, address, password) VALUES ('4', 'emp4', 'delta', '1234');
INSERT INTO librarian (librarian_id, name, address, password) VALUES ('5', 'emp5', 'alpha', '1234');
INSERT INTO librarian (librarian_id, name, address, password) VALUES ('6', 'emp6', 'beta', '1234');

INSERT INTO user (user_id, name, role, password, unpaid_fines, address) VALUES ('1', 'User1', 'student', '1234', 0.00, 'alpha');
INSERT INTO user (user_id, name, role, password, unpaid_fines, address) VALUES ('2', 'User2', 'student', '1234', 100.00, 'beta');
INSERT INTO user (user_id, name, role, password, unpaid_fines, address) VALUES ('3', 'User3', 'faculty', '1234', 0.00, 'gamma');
INSERT INTO user (user_id, name, role, password, unpaid_fines, address) VALUES ('4', 'User4', 'student', '1234', 100.00, 'delta');
INSERT INTO user (user_id, name, role, password, unpaid_fines, address) VALUES ('5', 'User5', 'student', '1234', 0.00, 'alpha');
INSERT INTO user (user_id, name, role, password, unpaid_fines, address) VALUES ('6', 'User6', 'faculty', '1234', 100.00, 'beta');

INSERT INTO books (isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id) VALUES ('1', 'author1', 'title1', 0.00,'AVAILABLE', 1, '2002', '1');
INSERT INTO books (isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id) VALUES ('12', 'author1', 'title1', 0.00,'AVAILABLE', 2, '2002', '1');
INSERT INTO books (isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id) VALUES ('13', 'author1', 'title1', 1.00,'AVAILABLE', 3, '2002', '1');
INSERT INTO books (isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id) VALUES ('14', 'author1', 'title1', 3.50,'AVAILABLE', 4, '2002', '1');
INSERT INTO books (isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id) VALUES ('15', 'author1', 'title1', 3.00,'AVAILABLE', 5, '2004', '1');
INSERT INTO books (isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id) VALUES ('16', 'author1', 'title1', 2.00,'UNAVAILABLE', 6, '2004', '1');
INSERT INTO books (isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id) VALUES ('21', 'author1', 'title21', 2.00,'ISSUED', 3, '2002', '1');
INSERT INTO books (isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id) VALUES ('22', 'author1', 'title22', 4.50,'AVAILABLE', 4, '2002', '1');
INSERT INTO books (isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id) VALUES ('23', 'author1', 'title23', 4.00,'AVAILABLE', 5, '2003', '1');
INSERT INTO books (isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id) VALUES ('24', 'author1', 'title24', 5.00,'ISSUED', 6, '2003', '1');
INSERT INTO books (isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id) VALUES ('25', 'author2', 'title25', 2.00,'ISSUED', 3, '2002', '1');
INSERT INTO books (isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id) VALUES ('26', 'author2', 'title26', 4.50,'AVAILABLE', 4, '2002', '1');
INSERT INTO books (isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id) VALUES ('27', 'author2', 'title27', 4.00,'AVAILABLE', 5, '2003', '1');
INSERT INTO books (isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id) VALUES ('28', 'author2', 'title28', 5.00,'ISSUED', 6, '2003', '1');
INSERT INTO books (isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id) VALUES ('2', 'author2', 'title2', 1.50,'UNAVAILABLE', 2, '2018', '1');
INSERT INTO books (isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id) VALUES ('3', 'author3', 'title3', 3.00,'ISSUED', 1, '2020', '1');
INSERT INTO books (isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id) VALUES ('4', 'author4', 'title4', 4.50,'AVAILABLE', 2, '2010', '2');
INSERT INTO books (isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id) VALUES ('5', 'author5', 'title5', 6.00,'UNAVAILABLE', 1, '2002', '2');
INSERT INTO books (isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id) VALUES ('6', 'author6', 'title6', 2.50,'ISSUED', 2, '2018', '3');

INSERT INTO shelf (shelf_id, capacity) VALUES ('1', 20);
INSERT INTO shelf (shelf_id, capacity) VALUES ('2', 2);
INSERT INTO shelf (shelf_id, capacity) VALUES ('3', 3);
INSERT INTO shelf (shelf_id, capacity) VALUES ('4', 4);
INSERT INTO shelf (shelf_id, capacity) VALUES ('5', 5);
INSERT INTO shelf (shelf_id, capacity) VALUES ('6', 1);

INSERT INTO genre (genre_id, name) VALUES ('1', 'crime');
INSERT INTO genre (genre_id, name) VALUES ('2', 'fiction');
INSERT INTO genre (genre_id, name) VALUES ('3', 'scifi');

INSERT INTO keeps_track (librarian_id, user_id) VALUES ('1', '1');
INSERT INTO keeps_track (librarian_id, user_id) VALUES ('2', '1');
INSERT INTO keeps_track (librarian_id, user_id) VALUES ('1', '2');
INSERT INTO keeps_track (librarian_id, user_id) VALUES ('2', '2');
INSERT INTO keeps_track (librarian_id, user_id) VALUES ('3', '2');
INSERT INTO keeps_track (librarian_id, user_id) VALUES ('4', '4');
INSERT INTO keeps_track (librarian_id, user_id) VALUES ('5', '5');
INSERT INTO keeps_track (librarian_id, user_id) VALUES ('6', '6');

INSERT INTO maintain (librarian_id, isbn) VALUES ('1', '1');
INSERT INTO maintain (librarian_id, isbn) VALUES ('1', '2');
INSERT INTO maintain (librarian_id, isbn) VALUES ('1', '3');
INSERT INTO maintain (librarian_id, isbn) VALUES ('2', '2');
INSERT INTO maintain (librarian_id, isbn) VALUES ('3', '3');
INSERT INTO maintain (librarian_id, isbn) VALUES ('4', '4');

INSERT INTO belongs_to (genre_id, isbn) VALUES ('1', '1');
INSERT INTO belongs_to (genre_id, isbn) VALUES ('1', '2');
INSERT INTO belongs_to (genre_id, isbn) VALUES ('2', '1');
INSERT INTO belongs_to (genre_id, isbn) VALUES ('3', '3');
INSERT INTO belongs_to (genre_id, isbn) VALUES ('3', '4');
INSERT INTO belongs_to (genre_id, isbn) VALUES ('2', '5');
INSERT INTO belongs_to (genre_id, isbn) VALUES ('1', '6');

INSERT INTO favourite (genre_id, user_id) VALUES ('1', '1');
INSERT INTO favourite (genre_id, user_id) VALUES ('2', '2');
INSERT INTO favourite (genre_id, user_id) VALUES ('3', '3');
INSERT INTO favourite (genre_id, user_id) VALUES ('1', '4');
INSERT INTO favourite (genre_id, user_id) VALUES ('2', '5');
INSERT INTO favourite (genre_id, user_id) VALUES ('3', '6');

INSERT INTO reading_list (isbn, user_id, name, list_url) VALUES ('1', '1', 'list1', 'abcd');
INSERT INTO reading_list (isbn, user_id, name, list_url) VALUES ('2', '1', 'list1', 'abcd');
INSERT INTO reading_list (isbn, user_id, name, list_url) VALUES ('3', '1', 'list2', 'ijkl');
INSERT INTO reading_list (isbn, user_id, name, list_url) VALUES ('4', '2', 'list3', 'mnop');
INSERT INTO reading_list (isbn, user_id, name, list_url) VALUES ('5', '3', 'list4', 'qrst');

INSERT INTO personal_book_shelf (isbn, user_id, shelf_name, shelf_url) VALUES ('1', '1', 'shelf1','abcd');
INSERT INTO personal_book_shelf (isbn, user_id, shelf_name, shelf_url) VALUES ('2', '1', 'shelf1','abcd');
INSERT INTO personal_book_shelf (isbn, user_id, shelf_name, shelf_url) VALUES ('3', '1', 'shelf2','ijkl');
INSERT INTO personal_book_shelf (isbn, user_id, shelf_name, shelf_url) VALUES ('4', '2', 'shelf3','mnop');
INSERT INTO personal_book_shelf (isbn, user_id, shelf_name, shelf_url) VALUES ('5', '3', 'shelf4','qrst');

INSERT INTO issue (isbn, user_id, due_date) VALUES ('1', '1', '2020-05-20');
INSERT INTO issue (isbn, user_id, due_date) VALUES ('2', '1', '2020-05-20');
INSERT INTO issue (isbn, user_id, due_date, issue_email_date) VALUES ('3', '2', '2020-04-24', '2020-04-14');
INSERT INTO issue (isbn, user_id, due_date, issue_email_date) VALUES ('4', '3', '2020-04-24', '2020-04-14');

INSERT INTO hold (isbn, user_id, hold_date, hold_email_date, hold_status) VALUES ('1', '1', '2020-04-24', '2020-04-14', 'ACCEPTED');
INSERT INTO hold (isbn, user_id, hold_date, hold_status) VALUES ('2', '1', '2020-04-24', 'PENDING');
INSERT INTO hold (isbn, user_id, hold_date, hold_email_date, hold_status) VALUES ('3', '2', '2020-04-14', '2020-04-20', 'ACCEPTED');
INSERT INTO hold (isbn, user_id, hold_date, hold_email_date, hold_status) VALUES ('4', '3', '2020-04-14', '2020-04-20', 'ACCEPTED');

INSERT INTO return_books (isbn, user_id, return_date, issue_date, fine) VALUES ('1', '1', '2020-05-24', '2020-05-20', 10.00);
INSERT INTO return_books (isbn, user_id, return_date, issue_date, fine) VALUES ('2', '1', '2020-04-30', '2020-04-20', 0.00);
INSERT INTO return_books (isbn, user_id, return_date, issue_date, fine) VALUES ('3', '2', '2020-04-24', '2020-04-14', 0.00);
INSERT INTO return_books (isbn, user_id, return_date, issue_date, fine) VALUES ('4', '3', '2020-04-24', '2020-04-14', 0.00);

INSERT INTO rate (isbn, user_id, rating, review) VALUES ('1', '1', 4.50, 'Best book for this subject!');
INSERT INTO rate (isbn, user_id, rating, review) VALUES ('2', '1', 1.00, ' latest edition has issues!');
INSERT INTO rate (isbn, user_id, rating, review) VALUES ('3', '2', 4.50, 'Best book for facts and GK!');
INSERT INTO rate (isbn, user_id, rating, review) VALUES ('4', '3', 5.00, 'Must read for 2nd year students!');

INSERT INTO friend (user_id, friend_id) VALUES ('1', '2');
INSERT INTO friend (user_id, friend_id) VALUES ('1', '3');
INSERT INTO friend (user_id, friend_id) VALUES ('1', '4');
INSERT INTO friend (user_id, friend_id) VALUES ('1', '5');
INSERT INTO friend (user_id, friend_id) VALUES ('2', '4');
INSERT INTO friend (user_id, friend_id) VALUES ('2', '6');
INSERT INTO friend (user_id, friend_id) VALUES ('3', '5');
## reverse
INSERT INTO friend (user_id, friend_id) VALUES ('2', '1');
INSERT INTO friend (user_id, friend_id) VALUES ('3', '1');
INSERT INTO friend (user_id, friend_id) VALUES ('5', '1');
INSERT INTO friend (user_id, friend_id) VALUES ('4', '2');
INSERT INTO friend (user_id, friend_id) VALUES ('6', '2');
INSERT INTO friend (user_id, friend_id) VALUES ('5', '3');

-- select * from librarian;
-- select * from user;
-- select * from books;
-- select * from shelf;