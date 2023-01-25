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




    CREATE_TABLE_DICT = {
        "users": """
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                chat_id INT,
                state BOOLEAN,
                last_visit DATE
            );""",

        "books": """
            CREATE TABLE IF NOT EXISTS books (
                book_id INT PRIMARY KEY,
                book_name VARCHAR(100) UNIQUE NOT NULL,
                book_info TEXT
            );""",

        "user_book": """
            CREATE TABLE IF NOT EXISTS user_book (
                user_book_id INT PRIMARY KEY,
                user_id INT NOT NULL,
                book_id INT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users (user_id),
                FOREIGN KEY(book_id) REFERENCES books (book_id)
            );""",
    
        "authors": """
            CREATE TABLE IF NOT EXISTS authors (
                author_id INT PRIMARY KEY,
                first_name VARCHAR(30),
                second_name VARCHAR(30),
                patronymic VARCHAR(30),
                info TEXT
            );""",
            
        "reviews": """
            CREATE TABLE IF NOT EXISTS reviews (
                review_id INT PRIMARY KEY,
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
                note_id INT PRIMARY KEY,
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
                user_book_id INT PRIMARY KEY,
                started_reading DATE,
                user_id INT NOT NULL,
                book_id INT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users (user_id),
                FOREIGN KEY(book_id) REFERENCES books (book_id)
            );""",

        "book_author": """
            CREATE TABLE IF NOT EXISTS book_author (
                book_author_id INT PRIMARY KEY,
                author_id INT NOT NULL,
                book_id INT NOT NULL,
                FOREIGN KEY(author_id) REFERENCES authors (author_id),
                FOREIGN KEY(book_id) REFERENCES books (book_id)
            );""",
    }

