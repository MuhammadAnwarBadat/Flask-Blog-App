# Flask Blog App

A simple blogging application built using Flask, PostgreSQL, and JWT authentication. Users can register, create blog posts, and add comments.

## Table of Contents
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Running the App](#running-the-app)
  - [Testing with Postman](#testing-with-postman)
    - [Register a New User (`api/register`)](#register-a-new-user-apiregister)
    - [Log In (`api/login`)](#log-in-apilogin)
    - [Create a New Blog Post (`api/create_post`)](#create-a-new-blog-post-apicreate_post)
    - [Create a Comment (`api/create_comment`)](#create-a-comment-apicreate_comment)
    - [View User's Blog Posts (`dashboard`)](#view-users-blog-posts-dashboard)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites

Make sure you have the following installed on your machine:

- [Python](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MuhammadAnwarBadat/Flask-Blog-App.git
   cd Flask-Blog-App

2. Create a virtual environment:
   ```bash
   python -m venv venv

3. Activate the virtual environment:
  - On Windows:
    ```bash
    venv\Scripts\activate
  - On macOS/Linux:
    ```bash
    source venv/bin/activate

4. Install dependencies:
   ```bash
   pip install -r requirements.txt

## Usage

### Running the App

1. Create the necessary database tables:
   ```bash
   python main.py

2. The app will run at http://127.0.0.1:5000/

### JWT (JSON Web Token) Authentication
This application uses JWT for user authentication. After registering or logging in, you will receive a JWT token in the response. Include this token in the Authorization header for subsequent requests to authenticate yourself

### Testing with Postman

1. Register a New User (api/register):
- Set the HTTP method to POST.
- Enter the URL: http://127.0.0.1:5000/api/register.
- Set the request body to JSON with the user registration details:
```json
{
  "username": "john_doe",
  "email": "john.doe@example.com",
  "password": "your_password"
}
```
- Click on the "Send" button.

2. Log In (api/login):
- Set the HTTP method to POST.
- Enter the URL: http://127.0.0.1:5000/api/login.
- Set the request body to JSON with the login details:
```json
{
  "email": "john.doe@example.com",
  "password": "your_password"
}
```
- Click on the "Send" button.

3. Create a New Blog Post (api/create_post):
- Set the HTTP method to POST.
- Enter the URL: http://127.0.0.1:5000/api/create_post.
- Set the request body to JSON with the post details:
```json
{
  "user_id": 1,  
  "title": "New Blog Post",
  "content": "This is the content of the blog post."
}
```
- Click on the "Send" button.

4. Create a Comment (api/create_comment):
- Set the HTTP method to POST.
- Enter the URL: http://127.0.0.1:5000/api/create_comment.
- Set the request body to JSON with the comment details:
```json
{
  "user_id": 1,  
  "post_id": 1,  
  "content": "This is a comment on the blog post."
}
```
- Click on the "Send" button.

### Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

### License
This project is licensed under the MIT License - see the LICENSE file for details.


