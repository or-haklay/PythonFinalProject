# Blog Application - Django REST API with React Frontend

A full-stack blog application built with Django REST Framework backend and React frontend, featuring user authentication, article management, and commenting system.

## Features

- **User Authentication**: JWT-based authentication with access and refresh tokens
- **User Groups**: Admin, Editors, and Regular Users with different permissions
- **Article Management**: Create, read, update, delete articles (editors and admins only)
- **Comment System**: Users can add and manage their own comments
- **Search Functionality**: Search articles by title, content, or tags
- **Responsive Design**: Modern React frontend with clean UI

## Project Structure

```
final/
├── api/                    # Django API app
│   ├── management/
│   │   └── commands/
│   │       └── setup_initial_data.py  # Database seeding command
│   ├── migrations/         # Database migrations
│   ├── models.py          # Data models
│   ├── serializers.py     # API serializers
│   ├── views.py           # API views
│   ├── urls.py            # API URL patterns
│   └── permissions.py     # Custom permissions
├── client/                 # React frontend
│   ├── public/
│   ├── src/
│   │   ├── App.js         # Main React component
│   │   ├── index.js       # React entry point
│   │   └── index.css      # Styles
│   └── package.json       # React dependencies
├── core/                   # Core utilities
│   └── auth.py            # JWT authentication
├── final/                  # Django project settings
│   ├── settings.py        # Django configuration
│   └── urls.py            # Main URL patterns
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL (or SQLite for development)
- pip (Python package manager)
- npm (Node package manager)

### Backend Setup (Django)

1. **Navigate to the project directory:**

   ```bash
   cd final
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the `final` directory with the following content:

   ```
   DB_NAME=blog_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. **Run database migrations:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create initial data (users, groups, sample content):**

   ```bash
   python manage.py setup_initial_data
   ```

7. **Create a superuser (optional):**

   ```bash
   python manage.py createsuperuser
   ```

8. **Start the Django development server:**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

### Frontend Setup (React)

1. **Navigate to the client directory:**

   ```bash
   cd client
   ```

2. **Install Node.js dependencies:**

   ```bash
   npm install
   ```

3. **Start the React development server:**
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000/`

## API Documentation

### Authentication Endpoints

#### Register User

- **POST** `/api/register/`
- **Description**: Register a new user
- **Body**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Registered successfully",
    "user": {
      "id": 1,
      "username": "string",
      "email": "string"
    },
    "access": "jwt_access_token",
    "refresh": "jwt_refresh_token"
  }
  ```

#### Login User

- **POST** `/api/token/`
- **Description**: Get JWT tokens for authentication
- **Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "access": "jwt_access_token",
    "refresh": "jwt_refresh_token"
  }
  ```

#### Refresh Token

- **POST** `/api/token/refresh/`
- **Description**: Get new access token using refresh token
- **Body**:
  ```json
  {
    "refresh": "jwt_refresh_token"
  }
  ```
- **Response**:
  ```json
  {
    "access": "new_jwt_access_token"
  }
  ```

### Articles Endpoints

#### Get All Articles

- **GET** `/api/articles/`
- **Description**: Get list of all articles
- **Query Parameters**:
  - `search`: Search articles by title, content, or tags
  - `page`: Page number for pagination
- **Response**:
  ```json
  {
    "count": 10,
    "next": "http://127.0.0.1:8000/api/articles/?page=2",
    "previous": null,
    "results": [
      {
        "id": 1,
        "title": "Article Title",
        "text": "Article content...",
        "author": {
          "id": 1,
          "user": {
            "username": "author_name"
          }
        },
        "tags": [
          {
            "id": 1,
            "name": "Django"
          }
        ],
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        "status": "published"
      }
    ]
  }
  ```

#### Get Single Article

- **GET** `/api/articles/{id}/`
- **Description**: Get a specific article by ID
- **Response**: Same as single article object above

#### Create Article (Editors/Admins Only)

- **POST** `/api/articles/`
- **Description**: Create a new article
- **Headers**:
  ```
  Authorization: Bearer jwt_access_token
  Content-Type: application/json
  ```
- **Body**:
  ```json
  {
    "title": "Article Title",
    "text": "Article content...",
    "tags": ["Django", "Python", "Tutorial"]
  }
  ```
- **Response**: Created article object

#### Update Article (Editors/Admins Only)

- **PUT** `/api/articles/{id}/`
- **Description**: Update an existing article
- **Headers**:
  ```
  Authorization: Bearer jwt_access_token
  Content-Type: application/json
  ```
- **Body**: Same as create article
- **Response**: Updated article object

#### Delete Article (Editors/Admins Only)

- **DELETE** `/api/articles/{id}/`
- **Description**: Delete an article
- **Headers**:
  ```
  Authorization: Bearer jwt_access_token
  ```
- **Response**: 204 No Content

### Comments Endpoints

#### Get Article Comments

- **GET** `/api/articles/{id}/comments/`
- **Description**: Get all comments for a specific article
- **Response**:
  ```json
  [
    {
      "id": 1,
      "text": "Great article!",
      "author": {
        "id": 1,
        "user": {
          "username": "commenter_name"
        }
      },
      "article": 1,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
  ```

#### Add Comment (Authenticated Users Only)

- **POST** `/api/articles/{id}/comments/`
- **Description**: Add a comment to an article
- **Headers**:
  ```
  Authorization: Bearer jwt_access_token
  Content-Type: application/json
  ```
- **Body**:
  ```json
  {
    "text": "Comment text..."
  }
  ```
- **Response**: Created comment object

#### Delete Comment (Comment Owner or Admin Only)

- **DELETE** `/api/comments/{id}/`
- **Description**: Delete a comment
- **Headers**:
  ```
  Authorization: Bearer jwt_access_token
  ```
- **Response**: 204 No Content

## User Groups and Permissions

### Admin Group

- Full access to all endpoints
- Can create, edit, and delete articles
- Can delete any comment
- Can manage users

### Editors Group

- Can create, edit, and delete articles
- Can delete any comment
- Can view all articles and comments

### Users Group

- Can view all articles
- Can add comments
- Can delete their own comments
- Cannot create or edit articles

## How to Create an Editor Account

### Method 1: Using Django Admin

1. Start the Django server: `python manage.py runserver`
2. Go to `http://127.0.0.1:8000/admin/`
3. Login with superuser credentials
4. Go to "Users" section
5. Create a new user or edit existing user
6. Add the user to "Editors" group

### Method 2: Using Management Command

The `setup_initial_data` command creates sample users including an editor:

- Username: `editor`
- Password: `editor123`
- Group: Editors

### Method 3: Using Django Shell

```python
python manage.py shell
```

```python
from django.contrib.auth.models import User, Group
from api.models import UserProfile

# Create user
user = User.objects.create_user(
    username='new_editor',
    email='editor@example.com',
    password='password123'
)

# Add to editors group
editors_group = Group.objects.get(name='Editors')
user.groups.add(editors_group)

# Create user profile
UserProfile.objects.create(user=user)
```

## Sample Data

The `setup_initial_data` management command creates:

### Users

- **Admin**: `admin` / `admin123` (Admin group)
- **Editor**: `editor` / `editor123` (Editors group)
- **User**: `user` / `user123` (Users group)

### Sample Articles

- "Getting Started with Django REST Framework"
- "Advanced Python Programming Techniques"
- "Building Modern Web Applications"

### Sample Comments

- 2 comments per article from the regular user

## Frontend Features

### Navigation

- Home page with latest 3 articles
- Login/Register links (when not authenticated)
- New Article link (when authenticated as editor/admin)
- Logout button (when authenticated)

### Article Management

- View all articles with search functionality
- View individual article details
- Create new articles (editors/admins only)
- Search articles by title, content, or tags

### Comment System

- View all comments for an article
- Add new comments (authenticated users only)
- Delete own comments
- Real-time comment updates

## Development Notes

### CORS Configuration

The Django backend is configured to allow requests from:

- `http://localhost:3000` (React dev server)
- `http://127.0.0.1:9000`
- `http://localhost:8080`
- `http://localhost:5173`

### JWT Token Configuration

- Access token lifetime: 60 minutes
- Refresh token lifetime: 7 days
- Token rotation enabled

### Database

- Default: PostgreSQL (configurable via environment variables)
- Fallback: SQLite for development

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'django'**

   - Make sure virtual environment is activated
   - Install requirements: `pip install -r requirements.txt`

2. **Database connection errors**

   - Check PostgreSQL is running
   - Verify database credentials in `.env` file
   - Run migrations: `python manage.py migrate`

3. **CORS errors in frontend**

   - Ensure Django server is running on port 8000
   - Check CORS_ALLOWED_ORIGINS in settings.py

4. **Authentication errors**
   - Verify JWT tokens are being sent in Authorization header
   - Check token expiration
   - Use refresh token to get new access token

### Getting Help

If you encounter issues:

1. Check the Django server logs
2. Check the React console for errors
3. Verify all environment variables are set correctly
4. Ensure all dependencies are installed

## License

This project is for educational purposes as part of a Django course final project.
