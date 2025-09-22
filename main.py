from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

class Base(DeclarativeBase):
  pass

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Books(db.Model):
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    title: Mapped[str] = mapped_column(String(25),unique=True, nullable=True)
    author: Mapped[str] = mapped_column(String(25),nullable=True)
    review: Mapped[float] = mapped_column(Float,nullable=True)

@app.route('/') 
def home():
    book = db.session.execute(db.select(Books).order_by(Books.id)).scalars()
    return render_template("index.html", all_books=book)

@app.route("/delete/<id>")
def delete(id):
    book_chose = db.session.execute(db.select(Books).where(Books.id==id)).scalar()
    db.session.delete(book_chose)
    db.session.commit()
    return redirect(url_for('home'))

    

@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):
    book_chose = db.session.execute(db.select(Books).where(Books.id==id)).scalar()
    if request.method == "POST":
        new_rating = request.form["edit_rating"]
        print(new_rating)
        book_chose.review = float(new_rating)
        print(book_chose.review)
        db.session.commit()  
        return redirect(url_for('home'))
    return render_template("rating.html",book=book_chose)


@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        book = Books(
            title=request.form["name"],
            author=request.form["author"],
            review=request.form["rating"]
        )
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('home'))
        # all_books.append(book)
    return render_template("add.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

