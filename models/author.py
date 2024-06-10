# lib/models/author.py
from database.connection import get_db_connection
from models.article import Article
from models.magazine import Magazine
class Author:
    def __init__(self, author_id, name):
        self.author_id = author_id
        self.name = name
        self._id =None
        self.create_author()
    def __repr__(self):
        return f'<Author {self.name}>'
    @property
    def id (self):
        return self._id 
    @id.setter
    def id(self, id):
     if  isinstance(id, int):
          self._id = id
     else :
         raise ValueError("Author id must be of type int")
     
     @property
     def name(self):
         return self._name
     @name.setter
     def name(self):
        if hasattr(self, '_name'):
            print("Cannot change the name after the author is instantiated.")
        elif isinstance(name, str) and len(name) > 0:
            self._name = name
        else:
            raise ValueError("Name must be of type  str.")
         
    
    def create_author(self):
        conn = get_db_connection()  # Get a connection to the database
        cursor = conn.cursor()      # Create a cursor object to execute SQL commands

        # Insert a new author into the authors table using self.name 
        cursor.execute('INSERT INTO authors ( name) VALUES (?)', ( self.name,))
        self._id =cursor.lastrowid
        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        
    
    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT articles.id, articles.title, articles.content, articles.author_id, articles.magazine_id
            FROM articles 
            JOIN authors  ON articles.author_id = authors.id
            JOIN magazines  ON articles.magazine_id = magazines.id
            WHERE authors.id = ?
        ''', (self.author_id,))
        
        rows = cursor.fetchall()
        conn.commit()
        
        return [Article(*row) for row in rows]

    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT magazines.id, magazines.name, mmagazines.category
            FROM magazines 
            JOIN articles  ON magazines.id = article.magazine_id
            JOIN authors  ON articles.author_id = authors.id
            WHERE authors.id = ?
        ''', (self.author_id,))
        
        rows = cursor.fetchall()
        conn.commit()
        
        return [Magazine(*row) for row in rows]