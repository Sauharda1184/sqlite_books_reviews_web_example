// Array to store book data
const books = [];

// Function to add a book to the list and send it to the server
function addBook() {
    const bookTitle = document.getElementById('bookTitle').value;
    const publicationYear = document.getElementById('publicationYear').value;

    // Create a JSON object with book data
    const bookData = {
        title: bookTitle,
        publication_year: publicationYear
    };

    // Send the book data to the server via POST request
    fetch('/api/add_book', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(bookData)
    })
        .then(response => response.json())
        .then(data => {
            // Display a success message or handle errors if needed
            console.log(data.message);

            // Add the new book data to the books array
            books.push(bookData);
            console.log(books)

            // Refresh the book list
            displayBooks();
        })
        .catch(error => {
            console.error('Error adding book:', error);
        });
}

// Function to display books in the list
function displayBooks() {
    const bookList = document.getElementById('bookList');
    bookList.innerHTML = ''; // Clear existing book list

    books.forEach(book => {
        const bookElement = document.createElement('div');
        bookElement.innerHTML = `
            <h2>Added Successfully :${book.title}</h2>
            <p>Publication Year: ${book.publication_year}</p>
        `;
        bookList.appendChild(bookElement);
    });
}

// Function to fetch and display all books from the server
function showAllBooks() {
    fetch('/api/books')
        .then(response => response.json())
        .then(data => {
            const bookList = document.getElementById('allbooks');
            bookList.innerHTML = ''; // Clear existing book list
            console.log(data)
            data.books.forEach(book => { // Access the 'books' key in the JSON response
                const bookElement = document.createElement('div');
                bookElement.innerHTML = `
                    <h2>${book.title}</h2>
                    <p>Publication Year: ${book.publication_year}</p>
                `;
                bookList.appendChild(bookElement);
            });
        })
        .catch(error => {
            console.error('Error fetching all books:', error);
        });
}

// Function to add a review for a book
function addReview(bookId) {
    const reviewText = document.getElementById(`reviewText_${bookId}`).value;

    const reviewData = {
        book_id: bookId,
        review_text: reviewText
    };

    fetch('/api/add_review', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(reviewData)
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            document.getElementById(`reviewText_${bookId}`).value = ''; // Clear input field
            showReviews(bookId); // Refresh reviews for the book
        })
        .catch(error => {
            console.error('Error adding review:', error);
        });
}

// Function to fetch and display reviews for a book
function showReviews(bookId) {
    fetch(`/api/get_reviews/${bookId}`)
        .then(response => response.json())
        .then(data => {
            const reviewsDiv = document.getElementById(`reviews_${bookId}`);
            reviewsDiv.innerHTML = ''; // Clear existing reviews
            data.reviews.forEach(review => {
                const reviewElement = document.createElement('div');
                reviewElement.innerHTML = `
                    <p>${review.review_text}</p>
                    <small>Reviewed on: ${review.review_date}</small>
                `;
                reviewsDiv.appendChild(reviewElement);
            });
        })
        .catch(error => {
            console.error('Error fetching reviews:', error);
        });
}
