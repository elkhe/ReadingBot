CREATE_USER = """
    INSERT INTO users(user_id, username, chat_id, state, last_visit) 
    VALUES (%s, %s, %s, %s, %s); 
"""

GET_USER = """
    SELECT user_id, username, chat_id, state, last_visit 
      FROM users
     WHERE user_id = %s;
"""

GET_BOOK_FROM_BOOKS = """
    SELECT book_id, book_name, author_name
      FROM books
     WHERE book_name = %s AND author_name = %s; 
"""

GET_BOOK_FROM_ACTIVE_LIST = """
    SELECT user_book_id
        FROM users INNER JOIN active_list
            ON users.user_id = active_list.user_id
        WHERE book_id = %s;
"""

#book_id int -> serial
CREATE_BOOK = """
    INSERT INTO books(book_name, author_name) 
    VALUES (%s, %s); 
"""

ADD_BOOK_TO_ACTIVE_LIST = """
    INSERT INTO active_list(book_id, user_id, started_reading) 
    VALUES (%s, %s, %s);
"""

GET_ACTIVE_LIST = """
    SELECT book_name, author_name 
    FROM users 
    INNER JOIN active_list
        ON users.user_id = active_list.user_id
    INNER JOIN books
        ON active_list.book_id = books.book_id
"""

DELETE_FROM_ALIST = """
    DELETE FROM active_list 
    WHERE book_id = %s;
"""