from flask import Flask, render_template, request, redirect, url_for, flash # type: ignore
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey"

# Initialize the SQLite database
def init_sqlite_db():
    conn = sqlite3.connect('library.db')
    conn.execute('CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER)')
    conn.close()

init_sqlite_db()

# Home Page - Display All Books
@app.route('/') # is a python decorator used in flask to associate a function with a particular URL
def index():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return render_template('index.html', books=books)

# Add a New Book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        
        if title and author and year:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
            conn.commit()
            conn.close()
            flash('Book added successfully!')
            return redirect(url_for('index'))
        else:
            flash('All fields are required!')
    return render_template('add_book.html')

# Update Book Details
@app.route('/update_book/<int:id>', methods=['GET', 'POST'])
def update_book(id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (id,))
    book = cursor.fetchone()
    conn.close()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']

        if title and author and year:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?", (title, author, year, id))
            conn.commit()
            conn.close()
            flash('Book updated successfully!')
            return redirect(url_for('index'))
        else:
            flash('All fields are required!')

    return render_template('update_book.html', book=book)

# Delete a Book
@app.route('/delete_book/<int:id>', methods=['GET'])
def delete_book(id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Book deleted successfully!')
    return redirect(url_for('index'))

# Search for a book
#@app.route('/search_book/')

if __name__ == '__main__':
    app.run(debug=True)