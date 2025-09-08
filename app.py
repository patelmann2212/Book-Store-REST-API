from flask import Flask, request, jsonify
from database import db
from models import Book
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import or_
from flasgger import Swagger



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)


with app.app_context():
    db.create_all()


def update_model(instance, data, fields):
    for field in fields:
        if field in data:
            setattr(instance, field, data[field])

# CREATE BOOK
@app.route("/books", methods=["POST"])
def create_book():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        # Basic validation
        if not data.get("title") or not data.get("author"):
            return jsonify({"error": "Title and Author are required"}), 400

        new_book = Book()
        update_model(new_book, data, [
            "title", "author", "publisher", "edition",
            "language", "pages", "genre", "price",
            "rating", "stock_status"
        ])

        db.session.add(new_book)
        db.session.commit()
        return jsonify(new_book.to_dict()), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Duplicate or constraint violation"}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET BOOKS
@app.route("/books", methods=["GET"])
def get_books():
    try:
        query = Book.query

        search = request.args.get("search")
        if search:
            query = query.filter(
                or_(
                    Book.title.ilike(f"%{search}%"),
                    Book.author.ilike(f"%{search}%"),
                    Book.genre.ilike(f"%{search}%")
                )
            )

        text_filters = {
            "title": Book.title,
            "author": Book.author,
            "genre": Book.genre
        }
        for param, column in text_filters.items():
            value = request.args.get(param)
            if value:
                query = query.filter(column.ilike(f"%{value}%"))

        min_price = request.args.get("min_price", type=float)
        max_price = request.args.get("max_price", type=float)
        if min_price is not None:
            query = query.filter(Book.price >= min_price)
        if max_price is not None:
            query = query.filter(Book.price <= max_price)

        books = query.all()
        return jsonify([b.to_dict() for b in books]), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# READ single book by id
@app.route("/books/id/<int:book_id>", methods=["GET"])
def get_book_by_id(book_id):
    try:
        book = Book.query.get_or_404(book_id, description="Book not found")
        return jsonify(book.to_dict()), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500


# READ all books by author (partial match allowed)
@app.route("/books/author/<string:book_author>", methods=["GET"])
def get_books_by_author(book_author):
    try:
        # Use case-insensitive partial match
        books = Book.query.filter(Book.author.ilike(f"%{book_author}%")).all()

        if not books:
            return jsonify({"error": f"No books found for author containing '{book_author}'"}), 404

        return jsonify([book.to_dict() for book in books]), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500




# UPDATE a book
@app.route("/books/id/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    try:
        book = Book.query.get_or_404(book_id, description="Book not found")
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        update_model(book, data, [
            "title", "author", "publisher", "edition",
            "language", "pages", "genre", "price",
            "rating", "stock_status"
        ])
        db.session.commit()
        return jsonify(book.to_dict()), 200

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Duplicate or constraint violation"}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# DELETE a book
@app.route("/books/id/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    try:
        book = Book.query.get_or_404(book_id, description="Book not found")
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book deleted successfully"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
