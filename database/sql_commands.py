class DatabaseCommands:
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
        SELECT book_id
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
        INSERT INTO active_list(started_reading, user_id, book_id) 
        VALUES (%s, %s, %s);
    """




#users user_id serial -> int 
    CREATE_TABLE_DICT = {
        "users": """
            CREATE TABLE IF NOT EXISTS users (
                user_id INT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                chat_id INT,
                state BOOLEAN,
                last_visit DATE
            );""",

        "books": """
            CREATE TABLE IF NOT EXISTS books (
                book_id SERIAL PRIMARY KEY,
                book_name VARCHAR(100) NOT NULL,
                author_name VARCHAR(30),
                book_info TEXT
            );""",

        "user_book": """
            CREATE TABLE IF NOT EXISTS user_book (
                user_book_id SERIAL PRIMARY KEY,
                user_id INT NOT NULL,
                book_id INT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users (user_id),
                FOREIGN KEY(book_id) REFERENCES books (book_id)
            );""",
    
            
        "reviews": """
            CREATE TABLE IF NOT EXISTS reviews (
                review_id SERIAL PRIMARY KEY,
                title_review VARCHAR(100),
                review_text TEXT, 
                score INT CHECK(score >= 0 AND score <= 10), 
                user_id INT NOT NULL,
                book_id INT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (book_id) REFERENCES books (book_id)
            );""",
            
        "notes": """
            CREATE TABLE IF NOT EXISTS notes (
                note_id SERIAL PRIMARY KEY,
                note_text TEXT,
                note_number INT,
                note_date DATE,
                user_id INT NOT NULL,
                book_id INT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users (user_id),
                FOREIGN KEY(book_id) REFERENCES books (book_id)
            );""",

        "active_list": """
            CREATE TABLE IF NOT EXISTS active_list (
                user_book_id SERIAL PRIMARY KEY,
                started_reading DATE,
                user_id INT NOT NULL,
                book_id INT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users (user_id),
                FOREIGN KEY(book_id) REFERENCES books (book_id)
            );"""
    }

