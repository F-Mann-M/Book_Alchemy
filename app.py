from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
import os
from datetime import date

# Builds the framework
app = Flask(__name__)

# Connet URI with DBMS
basedir = os.path.abspath(os.path.dirname(__file__))
# __file__ path of current python file
# os.path.dirname(path) the current folder that contains the file
# os.path.abspath() makes sure to get the absolut path

# creat connection to database with absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

# connect SQLAlchemy with app (Flask)
db.init_app(app)


@app.route("/", methods=["GET"]) # decorator
def home():
    books = db.session.query(Book).all()
    authors = db.session.query(Author).all()
    return render_template("home.html", books=books, authors=authors)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    message = "Add author."
    #get data from form
    if request.method == "POST":
        name = request.form.get("name")
        birthdate_str = request.form.get("birthdate")
        date_of_death_str = request.form.get("date_of_death")

        #convert date html values to python date
        birthdate = date.fromisoformat(birthdate_str) if birthdate_str else None
        date_of_death = date.fromisoformat(date_of_death_str) if date_of_death_str else None

        # add data to table
        new_author = Author(
            name = name,
            birth_date = birthdate,
            date_of_death = date_of_death)
        db.session.add(new_author)
        db.session.commit()
        message = f"Author {name} added successfully 'authors' table"

    return render_template("add_author.html", message=message)

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    message = "Add new Book"

    #get author_id
    authors = db.session.query(Author).all()

    #get data from form
    if request.method == "POST":
        isbn = request.form.get("isbn")
        title = request.form.get("title")
        year = request.form.get("year")
        author = request.form.get("author")

        print(author)
        #add book to table
        new_book = Book(
            isbn = isbn,
            title = title,
            publication_year = year,
            author_id = author)
        db.session.add(new_book)
        db.session.commit()
        message = f"Book '{title}' was successfully added to table 'books'."

    return render_template("add_book.html", message=message, authors=authors)

#creates tables
with app.app_context():
  db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)