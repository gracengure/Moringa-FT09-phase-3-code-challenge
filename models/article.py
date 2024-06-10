from database.connection import get_db_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        # Initialize the Article instance with the provided attributes
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def _repr_(self):
        # Return a string representation of the Article instance
        return f'<Article {self.title}>'

    @property
    def title(self):
        # Getter for the title property
        return self._title

    @title.setter
    def title(self, title):
        # Setter for the title property with validation
        if isinstance(title, str) and 5 <= len(title) <= 50:
            self._title = title
        else:
            raise ValueError("Title must be a string with length between 5 and 50 characters")

    def create_article(self):
        # Method to create a new article in the database
        conn = get_db_connection()  # Get a connection to the database
        cursor = conn.cursor()  # Create a cursor object to execute SQL commands
        sql = "INSERT INTO articles (author_id, magazine_id, title) VALUES (?, ?, ?)"
        cursor.execute(sql, (self.author_id, self.magazine_id, self.title))  # Execute the SQL command
        self.id = cursor.lastrowid  # Get the last inserted row ID
        conn.commit()  # Commit the transaction
        cursor.close()  # Close the cursor
        conn.close()  # Close the database connection

    def fetch_author(self):
        # Method to fetch the author of the article from the database
        conn = get_db_connection()  # Get a connection to the database
        cursor = conn.cursor()  # Create a cursor object to execute SQL commands
        sql = "SELECT authors.name FROM articles INNER JOIN authors ON articles.author_id = authors.id WHERE articles.id = ?"
        cursor.execute(sql, (self.id,))  # Execute the SQL command
        author = cursor.fetchone()  # Fetch the result
        
        conn.commit()  # Commit the transaction
        cursor.close()  # Close the cursor
        conn.close()  # Close the database connection

        if author:
            # Return the author's name if found
            return author[0]
        else:
            # Return None if no author is found
            return None

    def fetch_magazine(self):
        # Method to fetch the magazine of the article from the database
        conn = get_db_connection()  # Get a connection to the database
        cursor = conn.cursor()  # Create a cursor object to execute SQL commands
        sql = "SELECT magazines.name FROM articles INNER JOIN magazines ON articles.magazine_id = magazines.id WHERE articles.id = ?"
        cursor.execute(sql, (self.id,))  # Execute the SQL command
        magazine = cursor.fetchone()  # Fetch the result
        
        conn.commit()  # Commit the transaction
        cursor.close()  # Close the cursor
        conn.close()  # Close the database connection

        if magazine:
            # Return the magazine's name if found
            return magazine[0]
        else:
            # Return None if no magazine is found
            return None