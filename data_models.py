from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import foreign

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String,  nullable=False)
    birth_date = db.Column(db.Date)
    date_of_death = db.Column(db.Date)

    # create many to one relationship between author and books
    books = db.relationship("Book", back_populates="author", cascade="all, delete-orphan")


    def __repr__(self):
        return f"<Author(id={self.id}, name={self.name}>"


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.Integer)
    title = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, ForeignKey("authors.id"))

    # create  many to one relationship between books and author
    author = db.relationship("Author", back_populates="books")


    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}>"
