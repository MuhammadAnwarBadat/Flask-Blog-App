from flask import Flask, request, jsonify, session, redirect, url_for
import psycopg2
import os
from werkzeug.security import generate_password_hash, check_password_hash
import re
import jwt

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')


app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')
app.config['JWT_SECRET_KEY'] = 'e108ea7e3257455dae53344c22052b14'  # Change this to a secret key for security
# jwt = JWTManager(app)

def get_db_connection():
    return psycopg2.connect(
        dbname='blog_app_db',
        port="5432",
        user='postgres',
        password='qrc135zx',
        host='localhost'
    )

def create_user_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(80) UNIQUE NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password VARCHAR(200) NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            content TEXT NOT NULL,
            user_id INTEGER REFERENCES users(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            post_id INTEGER REFERENCES posts(id),
            user_id INTEGER REFERENCES users(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    connection.commit()
    connection.close()

def is_valid_email(email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None

def get_user_id(username):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch user ID based on the provided username
    cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
    user_id = cursor.fetchone()[0] if cursor.rowcount > 0 else None

    connection.close()

    return user_id

@app.route('/api/register', methods=['POST'])
def register_api():
    try:
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']

        # Validate email format
        if not is_valid_email(email):
            return jsonify({'error': 'Invalid email address'}), 400

        # Check for duplicate username or email
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s OR email = %s', (username, email))
        existing_user = cursor.fetchone()
        connection.close()

        if existing_user:
            return jsonify({'error': 'Username or email already exists'}), 400

        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Insert the new user into the database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)',
                       (username, email, hashed_password))
        connection.commit()
        connection.close()

        # Generate JWT token for the registered user
        user_id = get_user_id(username)
        if user_id is None:
            return jsonify({'error': 'Failed to retrieve user ID'}), 500

        jwt_token = jwt.encode({'user_id': user_id}, app.secret_key, algorithm='HS256')

        return jsonify({'message': 'Registration successful', 'token': jwt_token}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/create_post', methods=['POST'])
def create_post_api():
    try:
        user_id = request.json['user_id']
        title = request.json['title']
        content = request.json['content']

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('INSERT INTO posts (title, content, user_id) VALUES (%s, %s, %s)', (title, content, user_id))

        connection.commit()
        connection.close()

        return jsonify({'message': 'Post created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/login', methods=['POST'])
def login_api():
    try:
        email = request.json['email']
        password = request.json['password']

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()

        connection.close()

        if user and check_password_hash(user[3], password):
            # Password is correct, log the user in
            session['user_id'] = user[0]
            return jsonify({'message': 'Login successful'}), 200
        else:
            # Incorrect login credentials
            return jsonify({'error': 'Invalid email or password'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/api/create_comment', methods=['POST'])
def create_comment_api():
    try:
        user_id = request.json['user_id']
        post_id = request.json['post_id']
        content = request.json['content']

        if 'user_id' not in session:
            return jsonify({'error': 'User not logged in'}), 401

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('INSERT INTO comments (content, post_id, user_id) VALUES (%s, %s, %s)',
                       (content, post_id, user_id))

        connection.commit()
        connection.close()

        return jsonify({'message': 'Comment created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    user_id = session['user_id']

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('SELECT id, title, content FROM posts WHERE user_id = %s', (user_id,))
    posts = cursor.fetchall()

    posts_with_comments = []
    for post in posts:
        post_id = post[0]
        cursor.execute('SELECT id, content, user_id FROM comments WHERE post_id = %s', (post_id,))
        comments = cursor.fetchall()

        post_with_comments = list(post)
        post_with_comments.append(comments)
        posts_with_comments.append(tuple(post_with_comments))

    connection.close()

    return jsonify({'posts': posts_with_comments})

if __name__ == '__main__':
    create_user_table()
    app.run(debug=True)