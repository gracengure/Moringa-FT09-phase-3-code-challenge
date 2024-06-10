from database.connection import get_db_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id
    def _repr_(self):
        return f'<Article {self.title}>'    
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if isinstance(title, str) and 5 <= len(title) <= 50:
            self._title = title
        else:
            raise ValueError("Title must be a string with length between 5 and 50 characters")

    def create_article(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO articles (author_id, magazine_id, title) VALUES (?, ?, ?)"
        cursor.execute(sql, (self.author_id, self.magazine_id, self.title))
        self.id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()

    def fetch_author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT authors.name FROM articles INNER JOIN authors ON articles.author_id = authors.id WHERE articles.id = ?"
        cursor.execute(sql, (self.id,))
        author = cursor.fetchone()
        
        conn.commit()
        if author:
            return author[0]  
        else: return None
        
    def fetch_magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT magazine.name FROM articles INNER JOIN magazines ON articles.author_id = magazine.id WHERE articles.id = ?"
        cursor.execute(sql, (self.id,))
        magazine = cursor.fetchone()
        
        conn.commit()
        if magazine:
            return magazine[0]  
        else: return None
        
     
        