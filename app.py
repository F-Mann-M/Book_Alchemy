from flask import Flask, render_template, request
from data_models import db, Author, Book
import os
from datetime import date

# Builds the framework
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

# connect SQLAlchemy with app (Flask)
db.init_app(app)


@app.route("/", methods=["GET"]) # decorator
def home():
    """ return list of books to landing page"""
    books = db.session.query(Book).all()
    return render_template("home.html", books=books)


@app.route("/search", methods=["GET"])
def search():
    """ gets query parameters, search for title with similar content"""
    # get query parameters
    search_for = request.args.get("search", "")
    books = db.session.query(Book) \
        .filter(Book.title.like(f"%{search_for}%")) \
        .all()

    if not books:
        message = "Book not found"
    else:
        message = ""

    return render_template("home.html", books=books, message=message)

@app.route("/sorted", methods=["GET"])
def sort():
    """ Get request and return sorted book list"""
    sorted_list = []

    # get books
    books = db.session.query(Book).all()

    # get query parameters
    sort_by = request.args.get("sort", "title")

    # sort list by title, author or year
    if sort_by:
        if sort_by == "title":
            books.sort(key=lambda book: book.title)
        elif sort_by == "author":
            books.sort(key=lambda book: book.author.name)
        elif sort_by == "year":
            books.sort(key=lambda book: book.publication_year)

    return render_template("home.html", books=books)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    """
    Gets information about author from a html form (POST),
    add data to author table
    """
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
        message = f"Author {name} added successfully to database."

    return render_template("add_author.html", message=message)

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    """
    If GET request render add_book.html,
    if POST request collect data about book,
    add data to author table
    """

    message = "Add new Book"

    #get author_id
    authors = db.session.query(Author).all()

    #get data from form
    if request.method == "POST":
        try:
            isbn = request.form.get("isbn")
            title = request.form.get("title")
            year = request.form.get("year")
            author = request.form.get("author")

            if not isbn or not isbn.isdigit():
                raise ValueError("ISBN must be a number.")

            if not title:
                raise ValueError("Title is missing")

            if not year or not year.isdigit():
                raise ValueError("Year must be a number")

            #add book to table
            new_book = Book(
                isbn = isbn,
                title = title,
                publication_year = year,
                author_id = author)
            db.session.add(new_book)
            db.session.commit()
            message = f"Book '{title}' was successfully added to library."

        except ValueError as e:
            message = f"Error: {e}"

    return render_template("add_book.html", message=message, authors=authors)


@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    """
    Takes in book id by POST,
    checks if book with book_id is in database,
    deletes book form database,
    reloads library and returns to home
    """
    # delete book
    book = db.session.query(Book).filter(Book.id == book_id).first() #make sure book is in database
    if book:
        db.session.delete(book)
        db.session.commit()
        message = f"The book '{book.title}' has been removed successfully!"
    else:
        message = "Book not found in database"

    # fetch new list
    books = db.session.query(Book).all()
    return render_template("home.html", message=message, books=books)

#creates tables
# with app.app_context():
#   db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)