from bson import ObjectId
from flask import Flask,render_template,request, redirect,url_for
from pymongo import MongoClient
import config

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client[config.DATABASE_NAME]
books_collection =db[config.COLLECTION_NAME]

@app.route('/')
def index():
    books = list(books_collection.find())
    return render_template('index.html',books=books)

@app.route('/add',methods=['GET','POST'])
def add_book():
    if request.method == 'POST':
        book ={
            'title': request.form['title'],
            'author': request.form['author'],
            'year': request.form['year'],
            'genre': request.form['genre'],
        }
        books_collection.insert_one(book)
        return redirect(url_for('index'))
    return render_template("add_book.html")


@app.route('/update/<book_id>',methods=['GET','POST'])
def update_book(book_id):
    book = books_collection.find_one({'_id': ObjectId(book_id)})
    if request.method == 'POST':
        updated_book = {
            'title': request.form['title'],
            'author': request.form['author'],
            'year': request.form['year'],
            'genre': request.form['genre'],
        }
        books_collection.update_one({'_id': ObjectId(book_id)},{'$set':updated_book})
        return redirect(url_for('index'))
    return render_template('update_book.html',book=book, book_id=book_id )

@app.route('/delete/<book_id>', methods=['GET','POST'])
def delete_book(book_id):
    books_collection.delete_one({'_id': ObjectId(book_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)





