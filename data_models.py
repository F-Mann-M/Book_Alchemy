from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String,  nullable=False)
    birth_date = Column(Date)
    date_of_death = Column(Date)

    def __str__(self):
        return f"Author: {self.name}"

    def __repr__(self):
        return f"<Author(id={self.id}, name={self.name}>"


class Book(db.Model):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(Integer)
    title = Column(String, nullable=False)
    publication_year = (Integer)
    author_id = Column(Integer)

    def __str__(self):
        return f"Book: {self.title}"

    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}>"
