from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name, category):
        # Initialize the Magazine instance with the provided attributes
        self.id = id
        self.name = name
        self.category = category
        self.create_magazine()  # Create the magazine in the database

    def __repr__(self):
        # Return a string representation of the Magazine instance
        return f'<Magazine {self.name}>'

    @property
    def id(self):
        # Getter for the id property
        return self._id

    @id.setter
    def id(self, value):
        # Setter for the id property with validation
        if isinstance(value, int):
            self._id = value
        else:
            raise ValueError("Magazine id must be a type of int")

    @property
    def name(self):
        # Getter for the name property
        return self._name

    @name.setter
    def name(self, value):
        # Setter for the name property with validation
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        else:
            raise ValueError("Name must be a string of length 2 to 16")

    @property
    def category(self):
        # Getter for the category property
        return self._category

    @category.setter
    def category(self, value):
        # Setter for the category property with validation
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        else:
            raise ValueError("Category must be a non-empty string")

    def create_magazine(self):
        # Method to create a new magazine in the database
        conn = get_db_connection()  # Get a connection to the database
        cursor = conn.cursor()  # Create a cursor object to execute SQL commands
        sql = """
        INSERT INTO magazines (name, category) VALUES (?, ?)"""
        cursor.execute(sql, (self._name, self._category))  # Execute the SQL command
        self._id = cursor.lastrowid  # Get the last inserted row ID
        conn.commit()  # Commit the changes
        conn.close()  # Close the database connection

    def articles(self):
        # Method to fetch all articles associated with the magazine
        from models.article import Article  # Import the Article model
        conn = get_db_connection()  # Get a connection to the database
        cursor = conn.cursor()  # Create a cursor object to execute SQL commands
        cursor.execute("""
            SELECT articles.* 
            FROM articles 
            JOIN magazines ON articles.magazine_id = magazines.id 
            WHERE magazines.id = ?
        """, (self.id,))  # Execute the SQL command to fetch articles
        rows = cursor.fetchall()  # Fetch all rows from the executed query
        conn.close()  # Close the database connection
        return [Article(*row) for row in rows]  # Return a list of Article instances

    def contributors(self):
        # Method to fetch all unique authors who have written for the magazine
        from models.author import Author  # Import the Author model
        conn = get_db_connection()  # Get a connection to the database
        cursor = conn.cursor()  # Create a cursor object to execute SQL commands
        cursor.execute("""
            SELECT DISTINCT authors.id, authors.name 
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """, (self.id,))  # Execute the SQL command to fetch contributors
        rows = cursor.fetchall()  # Fetch all rows from the executed query
        conn.close()  # Close the database connection
        return [Author(*row) for row in rows]  # Return a list of Author instances

    def article_titles(self):
        # Method to fetch all article titles for the magazine
        conn = get_db_connection()  # Get a connection to the database
        cursor = conn.cursor()  # Create a cursor object to execute SQL commands
        cursor.execute("""
            SELECT title 
            FROM articles 
            WHERE magazine_id = ?
        """, (self.id,))  # Execute the SQL command to fetch article titles
        titles = [row[0] for row in cursor.fetchall()]  # Extract titles from the fetched rows
        conn.close()  # Close the database connection

        # Return the list of titles or None if there are no titles
        return titles if titles else None

    def contributing_authors(self):
        # Method to fetch all authors who have written more than 2 articles for the magazine
        from models.author import Author  # Import the Author model
        conn = get_db_connection()  # Get a connection to the database
        cursor = conn.cursor()  # Create a cursor object to execute SQL commands
        cursor.execute("""
            SELECT authors.*, COUNT(articles.id) as article_count 
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        """, (self.id,))  # Execute the SQL command to fetch contributing authors
        authors = cursor.fetchall()  # Fetch all rows from the executed query
        conn.close()  # Close the database connection

        # Return a list of Author instances if there are authors, otherwise return None
        return [Author(author['id'], author['name']) for author in authors] if authors else None
