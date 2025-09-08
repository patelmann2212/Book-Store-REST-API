
from database import db

class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    publisher = db.Column(db.String)
    edition = db.Column(db.String)
    language = db.Column(db.String)
    pages = db.Column(db.Integer)
    genre = db.Column(db.String)
    price = db.Column(db.Float)
    rating = db.Column(db.Float, default=0.0)
    stock_status = db.Column(db.String, default="available")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
