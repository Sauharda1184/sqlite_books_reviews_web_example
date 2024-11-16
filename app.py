from flask import Flask, jsonify, render_template, request
import sqlite3

app = Flask(__name__)

# Define the path to your SQLite database file
DATABASE = 'db/books.db'

@app.route('/api/books', methods=['GET'])
def get_all_books():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Books")
        books = cursor.fetchall()
        conn.close()

        # Convert the list of tuples into a list of dictionaries
        book_list = []
        for book in books:
            book_dict = {
                'book_id': book[0],
                'title': book[1],
                'publication_year': book[2]
                # Add other attributes here as needed
            }
            book_list.append(book_dict)

        return jsonify({'books': book_list})
    except Exception as e:
        return jsonify({'error': str(e)})


# API to get all authors
@app.route('/api/authors', methods=['GET'])
def get_all_authors():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Authors")
        authors = cursor.fetchall()
        conn.close()
        return jsonify(authors)
    except Exception as e:
        return jsonify({'error': str(e)})

# API to get all reviews
@app.route('/api/reviews', methods=['GET'])
def get_all_reviews():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Reviews")
        reviews = cursor.fetchall()
        conn.close()
        return jsonify(reviews)
    except Exception as e:
        return jsonify({'error': str(e)})

# API to add a book to the database
@app.route('/api/add_book', methods=['POST'])
def add_book():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Get book details from the request
        data = request.get_json()
        title = data.get('title')
        publication_year = data.get('publication_year')

        # Insert the book into the database
        cursor.execute("INSERT INTO Books (title, publication_year) VALUES (?, ?)", (title, publication_year))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Book added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})


# API to add a review for a book
@app.route('/api/add_review', methods=['POST'])
def add_review():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get review details from the request
        data = request.get_json()
        book_id = data.get('book_id')
        review_text = data.get('review_text')

        # Insert the review into the database
        cursor.execute("INSERT INTO Reviews (book_id, review_text) VALUES (?, ?)", (book_id, review_text))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Review added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

# API to get reviews for a specific book
@app.route('/api/get_reviews/<int:book_id>', methods=['GET'])
def get_reviews_for_book(book_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT review_text, review_date FROM Reviews WHERE book_id = ?", (book_id,))
        reviews = cursor.fetchall()
        conn.close()

        # Convert to list of dictionaries
        reviews_list = [{'review_text': review['review_text'], 'review_date': review['review_date']} for review in reviews]

        return jsonify({'reviews': reviews_list})
    except Exception as e:
        return jsonify({'error': str(e)})

# Route to render the index.html page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
