# Book-Store-REST-API

📚 Book Store REST API

A simple RESTful API built with Flask (or your framework of choice) to manage a bookstore.
This API allows users to perform CRUD (Create, Read, Update, Delete) operations on books.

🚀 Features

Add a new book
Get all books
Get a single book by ID or author
Update book details
Delete a book
Error handling for invalid requests

🛠️ Tech Stack

Backend Framework: Flask
Database: SQLAlchemy (SQLite / MySQL / PostgreSQL)
Language: Python 3.x
Tools: Postman for testing


📖 API Endpoints
Books

Method	Endpoint	    Description
GET	    /books	      Get all books
GET	    /books/id/<id>	  Get book by ID
GET	    /books/author/<name>	Get book by author
POST	  /books	      Add a new book
PUT	    /books/id/<id>	  Update book details
DELETE	/books/id/<id>	  Delete a book
