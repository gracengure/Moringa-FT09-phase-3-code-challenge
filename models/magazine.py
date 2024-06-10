from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name, category):
    
        self.id=id
        self.name = name
        self.category = category
        self.create_magazine()
    def __repr__(self):
        return f'<Magazine {self.name}>'    
    @property
    def id (self):
        return self._id 
    def id(self, value):
        if isinstance(value, int):
            self._id = value
        else:
            raise ValueError("Magazine id must be a type of int")

    @property
    def name (self):
        return self._id
    
    @name.setter
    def name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        else:
            raise ValueError("Name must be a string of length 2 to 16")

    @property
    def category(self):
         return self._category
    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        else:
            raise ValueError("Category must be a non-empty string")



    def create_magazine(self):
        conn = get_db_connection()  # Get a connection to the database
        cursor = conn.cursor()      # Create a cursor object to execute SQL commands
        sql= """
        INSERT INTO magazines (name , category) VALUES (?,?)"""
        cursor.execute(sql ,(self._name, self._category))
        self._id= cursor.lastrowid
        conn.commit()
        

    def articles(self):
     from models.article import Article

     conn = get_db_connection()
     cursor = conn.cursor()
     cursor.execute("""
        SELECT articles.* 
        FROM articles 
        JOIN magazines ON articles.magazine_id = magazines.id 
        WHERE magazines.id = ?
        """, (self.id,))
     rows = cursor.fetchall()
     conn.close()
     return [Article(*row) for row in rows] 
    
    def contributors(self):
        from models.author import Author
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
             SELECT DISTINCT authors.id, authors.name 
        FROM authors
        JOIN articles ON authors.id = articles.author_id
        WHERE articles.magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.commit()
        return [Author(*row) for row in rows]
    def article_titles(self):
     conn = get_db_connection()
     cursor = conn.cursor()
     cursor.execute("""
        SELECT title 
        FROM articles 
        WHERE magazine_id = ?
    """, (self.id,))
     titles = [row[0] for row in cursor.fetchall()]
     conn.close()
    
     if titles:
        return titles
     else:
        return None
     
    def contributing_authors(self):
        from models.author import Author
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT authors.*, COUNT(articles.id) as article_count FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        """, (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return [Author(author['id'], author['name']) for author in authors] if authors else None