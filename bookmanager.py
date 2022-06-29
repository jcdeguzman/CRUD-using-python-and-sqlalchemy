import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database = f"mysql://pul:admin@localhost/practice_crud"
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):

    __tablename__ = "book"

    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    
    def __repr__(self):
        return "<Title: {}>".format(self.title)

@app.route('/', methods=["GET", "POST"])
def home():
    books = None
    if request.form:
        try:
            title = request.form.get("title")
            author = request.form.get("author")
            book = Book(title=title, author=author)
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            print("Failed to add book")
            print(e)
    books = Book.query.all()
    return render_template("home.html", books=books)

@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        newauthor = request.form.get("newauthor")
        oldtitle = request.form.get("oldtitle")
        oldauthor = request.form.get("oldauthor")
        book = Book.query.filter_by(title=oldtitle).first()
        book = Book.query.filter_by(author=oldauthor).first()
        book.title = newtitle
        book.author = newauthor
        db.session.commit()
    except Exception as e:
        print("Couldn't update book title")
        print(e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    id = request.form.get("id")
    book = Book.query.filter_by(id=id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)