# lib/models/author.py
from database.connection import get_db_connection
from models.article import Article
from models.magazine import Magazine
class Author:
    def __init__(self, author_id, name):
        # Initialize the Author instance with the provided attributes
        self.author_id = author_id
        self.name = name
        self._id = None  # Initialize _id as None
        self.create_author()  # Create the author in the database

    def __repr__(self):
        # Return a string representation of the Author instance
        return f'<Author {self.name}>'

    @property
    def id(self):
        # Getter for the id property
        return self._id

    @id.setter
    def id(self, id):
        # Setter for the id property with validation
        if isinstance(id, int):
            self._id = id
        else:
            raise ValueError("Author id must be of type int")

    @property
    def name(self):
        # Getter for the name property
        return self._name

    @name.setter
    def name(self, name):
        # Setter for the name property with validation
        if hasattr(self, '_name'):
            print("Cannot change the name after the author is instantiated.")
        elif isinstance(name, str) and len(name) > 0:
            self._name = name
        else:
            raise ValueError("Name must be of type str.")

    def create_author(self):
        # Method to create a new author in the database
        conn = get_db_connection()  # Get a connection to the database
        cursor = conn.cursor()  # Create a cursor object to execute SQL commands

        # Insert a new author into the authors table using self.name
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (self.name,))
        self._id = cursor.lastrowid  # Get the last inserted row ID

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

    def articles(self):
        # Method to fetch all articles written by the author
        conn = get_db_connection()  # Get a connection to the database
        cursor = conn.cursor()  # Create a cursor object to execute SQL commands

        # Execute a SQL command to fetch articles written by the author
        cursor.execute('''
            SELECT articles.id, articles.title, articles.content, articles.author_id, articles.magazine_id
            FROM articles 
            JOIN authors ON articles.author_id = authors.id
            JOIN magazines ON articles.magazine_id = magazines.id
            WHERE authors.id = ?
        ''', (self.author_id,))

        rows = cursor.fetchall()  # Fetch all rows from the executed query
        conn.commit()  # Commit the changes
        conn.close()  # Close the database connection

        # Return a list of Article instances
        return [Article(*row) for row in rows]

    def magazines(self):
        # Method to fetch all magazines in which the author has articles
        conn = get_db_connection()  # Get a connection to the database
        cursor = conn.cursor()  # Create a cursor object to execute SQL commands

        # Execute a SQL command to fetch magazines in which the author has articles
        cursor.execute('''
            SELECT DISTINCT magazines.id, magazines.name, magazines.category
            FROM magazines 
            JOIN articles ON magazines.id = articles.magazine_id
            JOIN authors ON articles.author_id = authors.id
            WHERE authors.id = ?
        ''', (self.author_id,))

        rows = cursor.fetchall()  # Fetch all rows from the executed query
        conn.commit()  # Commit the changes
        conn.close()  # Close the database connection

        # Return a list of Magazine instances
        return [Magazine(*row) for row in rows]
