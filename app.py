import os
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from celery import Celery, shared_task
import redis
import models
from celery.schedules import crontab
from flask_mail import Mail, Message

# Configure Flask and Celery
app = Flask(__name__)
CORS(app)

# Flask configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
broker_connection_retry_on_startup = True

# Initialize Redis and Celery
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Initialize the database
db = models.db
db.init_app(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  # For TLS
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('smtptest2048@gmail.com')  # Your email
app.config['MAIL_PASSWORD'] = os.environ.get('qwerty@1')  # Your email password
DEFAULT_FROM_EMAIL = 'email@yourserver.com'
SERVER_EMAIL = 'email@yourserver.com'
mail = Mail(app)

# Security answer for admin signup
ADMIN_SECURITY_ANSWER = "your_admin_code"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.before_request
def create_tables():
    if not hasattr(app, 'has_run'):
        with app.app_context():
            db.create_all()
        app.has_run = True

@app.before_request
def create_admin():
    with app.app_context():
        # Check if an admin already exists
        admin_email = "admin@dummy.com"
        admin_password = "admin123"
        
        existing_admin = models.User.query.filter_by(email=admin_email).first()
        if existing_admin is None:
            hashed_password = generate_password_hash(admin_password, method='pbkdf2:sha256')
            admin_user = models.User(
                name="Admin", 
                email=admin_email, 
                password=hashed_password,
                mobile_number="1234567890",
                bio="Administrator of the E-Library app",
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created")
        else:
            print("Admin user already exists")

@shared_task
def test_task():
    return "Celery is working!"

# Celery task to automatically return overdue books
@shared_task
def auto_return_books():
    with app.app_context():
        overdue_borrows = models.Borrow.query.filter(
            models.Borrow.due_date < datetime.now().date(),
            models.Borrow.return_date.is_(None)
        ).all()

        for borrow in overdue_borrows:
            borrow.return_date = datetime.now().date()
            db.session.add(borrow)

        db.session.commit()

        return f"Auto-returned {len(overdue_borrows)} books."
    
@shared_task
def send_email_reminders():
    with app.app_context():
        users = models.User.query.all()
        today = datetime.now().date()

        for user in users:
            if user.last_login is not None:
                msg = Message("We Missed You!", sender='smtptest2048@gmail.com', recipients=[user.email])
                msg.body = "Hello, we noticed you haven't logged in today. We miss you at the library!"
                mail.send(msg)
    
@shared_task
def send_monthly_borrowed_books_email():
    with app.app_context():
        # Get the first day of the current month
        first_day_of_month = datetime.now().replace(day=1)
        # Get the last day of the previous month
        last_day_of_previous_month = first_day_of_month - timedelta(days=1)
        
        users = models.User.query.all()

        for user in users:
            borrowed_books = models.Borrow.query.filter(
                models.Borrow.user_id == user.id,
                models.Borrow.borrowed_date >= first_day_of_month - timedelta(days=last_day_of_previous_month.day),
                models.Borrow.borrowed_date <= last_day_of_previous_month
            ).all()

            if borrowed_books:
                book_titles = [book.book.title for book in borrowed_books]
                msg = Message("Your Monthly Borrowed Books", sender='smtptest@gmail.com', recipients=[user.email])
                msg.body = f"Hello {user.name},\n\nHere are the books you borrowed this month:\n" + "\n".join(book_titles) + "\n\nThank you for using our library!"
                mail.send(msg)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls auto_return_books every day at 00:00 (midnight)
    sender.add_periodic_task(crontab(hour=0, minute=0), auto_return_books.s())
    # Calls send_email_reminders every day at 09:00 AM
    sender.add_periodic_task(crontab(hour=9, minute=0), send_email_reminders.s())
    # Calls send_monthly_borrowed_books_email on the first day of every month at 10:00 AM
    sender.add_periodic_task(crontab(hour=10, minute=0, day_of_month='1'), send_monthly_borrowed_books_email.s())


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = models.User(
        email=data['email'],
        password=hashed_password,
        is_admin=False,
        name=data['name'],
        mobile_number=data['mobile']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/admin-signup', methods=['POST'])
def admin_signup():
    data = request.get_json()
    if data['securityAnswer'] != ADMIN_SECURITY_ANSWER:
        return jsonify({'message': 'Invalid security answer'}), 401
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_admin = models.User(
        email=data['email'],
        password=hashed_password,
        is_admin=True,
        name=data['name'],
        mobile_number=data['mobile']
    )
    db.session.add(new_admin)
    db.session.commit()
    return jsonify({'message': 'Admin created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = models.User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
 

    user.last_login = datetime.now()  # Update last_login
    db.session.commit()

    session['user_id'] = user.id
    session['user_name'] = user.name
    session['is_admin'] = user.is_admin

    return jsonify({
        'message': 'Logged in successfully',
        'user': {
            'id': user.id,
            'email': user.email,
            'is_admin': user.is_admin,  # Include this in the response
            'name': user.name,
            'mobile': user.mobile_number
        }
    }), 200

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('is_admin', None)
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/categories', methods=['POST'])
def add_category():
    data = request.get_json()
    new_category = models.Category(name=data['name'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message': 'Category added successfully'}), 201

@app.route('/books', methods=['POST'])
def add_book():
    data = request.form
    file = request.files.get('cover_image')
    file2 = request.files.get('pdf_file')  # Get the PDF file
    cover_image = None
    pdf_file = None

    # Upload cover image
    if file and allowed_file(file.filename):  # Define valid extensions for images
        filename = secure_filename(file.filename)
        # Create the upload directory if it doesn't exist
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        cover_image = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Upload PDF file
    if file2 and allowed_file(file2.filename):  # Ensure it's a valid PDF
        file2name = secure_filename(file2.filename)
        # Create the upload directory if it doesn't exist
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        file2.save(os.path.join(app.config['UPLOAD_FOLDER'], file2name))
        pdf_file = os.path.join(app.config['UPLOAD_FOLDER'], file2name)

    # Create the new book entry with the uploaded files' paths
    new_book = models.Book(
        title=data['title'],
        author=data['author'],
        description=data.get('description'),
        cover_image=cover_image,
        category_id=data['category_id'],
        pdf_file=pdf_file  # Save the PDF path
    )

    # Commit the book to the database
    db.session.add(new_book)
    db.session.commit()

    return jsonify({'message': 'Book added successfully'}), 201

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = models.Category.query.all()
    return jsonify([{'id': category.id, 'name': category.name} for category in categories])

@app.route('/books', methods=['GET'])
def get_books():
    categories = models.Category.query.all()
    result = []
    for category in categories:
        books = models.Book.query.filter_by(category_id=category.id).all()
        books_list = [{
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'description': book.description,
            'cover_image': request.host_url + book.cover_image  # Include the full URL
        } for book in books]
        result.append({
            'category': category.name,
            'books': books_list
        })
    return jsonify(result)

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = models.Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'description': book.description,
        'cover_image': request.host_url + book.cover_image,  # Include full URL
        'pdf_file': request.host_url + book.pdf_file if book.pdf_file else None,  # Include full URL of the PDF
        'category_id': book.category_id
    })


@app.route('/borrow', methods=['POST'])
def borrow_book():
    data = request.get_json()
    
    # Get the user_id and book_id from the request data
    user_id = data.get('user_id')
    book_id = data.get('book_id')
    
    # Ensure both user_id and book_id are present
    if not user_id or not book_id:
        return jsonify({'message': 'User ID and Book ID are required'}), 400
    
    # Query to check how many books the user has currently borrowed and not returned
    active_borrow_count = models.Borrow.query.filter_by(user_id=user_id, return_date=None).count()

    # Enforce the limit of 5 books per user
    if active_borrow_count >= 5:
        return jsonify({'message': 'You have already borrowed the maximum number of books (5). Please return a book before borrowing another.'}), 403

    # Check if the borrowed_date is present in the request
    borrowed_date_str = data.get('borrowed_date')
    if borrowed_date_str:
        borrowed_date = datetime.strptime(borrowed_date_str, '%Y-%m-%dT%H:%M:%S.%fZ').date()
    else:
        return jsonify({'message': 'Borrowed date is required'}), 400

    # Set due date 7 days from borrowed date
    due_date = borrowed_date + timedelta(days=7)

    # Create a new Borrow entry
    new_borrow = models.Borrow(
        user_id=user_id,
        book_id=book_id,
        borrowed_date=borrowed_date,
        due_date=due_date
    )
    
    # Add the new borrow entry to the database
    db.session.add(new_borrow)
    db.session.commit()
    
    return jsonify({'message': 'Book borrowed successfully'}), 201


@app.route('/return', methods=['POST'])
def return_book():
    data = request.get_json()
    borrow_record = models.Borrow.query.filter_by(user_id=data['user_id'], book_id=data['book_id'], return_date=None).first()
    if not borrow_record:
        return jsonify({'message': 'Borrow record not found'}), 404
    borrow_record.return_date = datetime.strptime(data['return_date'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
    db.session.commit()
    return jsonify({'message': 'Book returned successfully'}), 200

@app.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    user = models.User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'mobile': user.mobile_number,
        'bio': user.bio,
        'photo': user.profile_photo
    })

# app.py
@app.route('/borrowed-books/<int:user_id>', methods=['GET'])
def get_borrowed_books(user_id):
    borrowed_books = models.Borrow.query.filter_by(user_id=user_id, return_date=None).all()
    books = []
    for borrow in borrowed_books:
        book = models.Book.query.get(borrow.book_id)
        if book:
            books.append({
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'cover_image': request.host_url + book.cover_image,
                'borrowed_date': borrow.borrowed_date.isoformat(),
                'due_date': borrow.due_date.isoformat()
            })
    return jsonify(books)

@app.route('/returned-books/<int:user_id>', methods=['GET'])
def get_returned_books(user_id):
    returned_books = models.Borrow.query.filter_by(user_id=user_id).filter(models.Borrow.return_date.isnot(None)).all()
    books = []
    for borrow in returned_books:
        book = models.Book.query.get(borrow.book_id)
        if book:
            books.append({
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'cover_image': request.host_url + book.cover_image,
                'borrowed_date': borrow.borrowed_date.isoformat(),
                'returned_date': borrow.return_date.isoformat()
            })
    return jsonify(books)

# Fetch users and their borrowed books
@app.route('/users-with-books', methods=['GET'])
def get_users_with_books():
    users_with_books = []
    users = models.User.query.all()

    for user in users:
        borrowed_books = models.Borrow.query.filter_by(user_id=user.id).all()
        for borrow in borrowed_books:
            book = models.Book.query.get(borrow.book_id)
            users_with_books.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'borrowed_book': {
                    'id': book.id,
                    'title': book.title
                },
                'borrowed_date': borrow.borrowed_date
            })

    return jsonify(users_with_books), 200

# Revoke a user's access to a borrowed book
@app.route('/revoke-access', methods=['POST'])
def revoke_access():
    data = request.get_json()
    user_id = data['user_id']
    book_id = data['book_id']

    borrow = models.Borrow.query.filter_by(user_id=user_id, book_id=book_id).first()
    
    if borrow:
        db.session.delete(borrow)
        db.session.commit()
        return jsonify({'message': 'Access revoked successfully'}), 200
    else:
        return jsonify({'message': 'Borrow record not found'}), 404

@app.route('/books_stats', methods=['GET'])
def get_books_stats():
    books_stats = db.session.query(
        models.Book.title,
        db.func.count(models.Borrow.book_id).label('num_borrowed'),
        db.func.count(models.Borrow.user_id).label('num_users')
    ).join(models.Borrow).group_by(models.Book.title).all()

    # Convert to a list of dictionaries for easier use in Vue.js
    stats = [{'title': title, 'num_borrowed': num_borrowed, 'num_users': num_users} for title, num_borrowed, num_users in books_stats]
    return jsonify(stats)


@app.route('/admin-dashboard', methods=['GET'])
def admin_dashboard():
    total_books = models.Book.query.count()
    total_users = models.User.query.count()
    total_borrows = models.Borrow.query.count()
    overdue_borrows = models.Borrow.query.filter(models.Borrow.due_date < datetime.now().date(), models.Borrow.return_date.is_(None)).count()

    return jsonify({
        'total_books': total_books,
        'total_users': total_users,
        'total_borrows': total_borrows,
        'overdue_borrows': overdue_borrows
    })

@app.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get(id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully'})
    return jsonify({'message': 'Category not found'}), 404

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'})
    return jsonify({'message': 'Book not found'}), 404


@app.route('/api/update-profile', methods=['PUT'])
def update_profile():
    data = request.get_json()
    user = models.User.query.get(data['id'])
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user.name = data['name']
    user.mobile_number = data['mobile']
    user.bio = data['bio']
    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'})

@app.route('/api/upload-profile-photo', methods=['POST'])
def upload_profile_photo():
    user_id = request.form['user_id']
    file = request.files.get('profile_photo')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        user = models.User.query.get(user_id)
        user.profile_photo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        db.session.commit()
        return jsonify({'profile_photo': user.profile_photo}), 200
    return jsonify({'message': 'Invalid file type'}), 400

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    user_id = session.get('user_id')  # Assuming user is logged in
    if user_id:
        notifications = []
        keys = redis_client.keys(f'overdue_notification:{user_id}:*')
        for key in keys:
            notification = redis_client.get(key)
            notifications.append(notification.decode('utf-8'))  # Redis stores data as bytes
        return jsonify(notifications)
    else:
        return jsonify({"error": "User not logged in"}), 401

# Start auto-return task route
@app.route('/auto-return', methods=['POST'])
def auto_return():
    task = auto_return_books.delay()  # Call the Celery task
    return jsonify({'task_id': task.id, 'status': 'Task started'}), 202

if __name__ == '__main__':
    app.run(debug=True)
