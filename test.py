from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float





app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db = SQLAlchemy(app)

class book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=True)
    author = db.Column(db.String(20), unique=True, nullable=True)
    review = db.Column(db.Integer, unique=True, nullable=True)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        a = book(id=1,title="Harry Potter", author="JK", review=9)
        db.session.add(a)
        db.session.commit()
        app.run()