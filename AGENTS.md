# AGENTS.md

**Purpose**: Compact instruction file for future OpenCode sessions to avoid mistakes and ramp up quickly.

---

## 🚀 Quick Start

```bash
# Clone and run (development)
git clone <repo-url> && cd website-cource-auth
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
./run.sh
```

The app runs at `http://localhost:8000` with auto-reload enabled.

---

## 📦 Architecture & Entry Points

### Framework & Stack
- **Backend**: FastAPI 0.109.0 (Python web framework)
- **Database**: SQLAlchemy 2.0.25 (ORM) with SQLite (courses.db)
- **Auth**: JWT tokens with python-jose[cryptography] 3.3.0
- **Passwords**: bcrypt via passlib[bcrypt] 1.7.4
- **Templates**: Jinja2 3.1.3
- **Server**: Uvicorn 0.27.0 (ASGI server)

### Entry Points
- **Main application**: `app/main.py` - FastAPI app initialization and routes
- **Database**: `app/database.py` - SQLAlchemy models and initialization
- **Auth**: `app/auth.py` - JWT token handling, password verification, user auth middleware

### Key Files
```
website-cource-auth/
├── app/
│   ├── main.py          # FastAPI routes and HTML templates
│   ├── auth.py          # Authentication logic (login, logout, JWT)
│   ├── database.py      # SQLAlchemy models and DB initialization
│   ├── static/          # Static assets (JavaScript, CSS)
│   └── templates/       # HTML templates (currently unused, inline in main.py)
├── courses.db           # SQLite database (auto-created)
├── requirements.txt     # Python dependencies
├── run.sh               # Development server startup script
└── venv/                # Python virtual environment
```

---

## ⚙️ Developer Commands

### Development Server
```bash
# Start development server (auto-reload, port 8000)
./run.sh

# Or manually:
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Database Operations
```bash
# Initialize/reset database with sample courses
python -c "from app.database import init_db; init_db()"

# The database file is SQLite: courses.db (created automatically)
```

### Testing
```bash
# Run test files
python test_auth_fix.py
python test_e2e_login.py
python debug_login.py
python debug_token.py

# Note: Tests require the database to be initialized first
```

---

## 🔐 Authentication Flow

### JWT Token Setup
- **Secret**: `SECRET_KEY` in `app/database.py` (change in production!)
- **Algorithm**: HS256
- **Expiry**: 30 minutes (`ACCESS_TOKEN_EXPIRE_MINUTES`)
- **Storage**: HTTP-only cookie named `access_token`
- **Cookie settings**:
  - `max_age`: 7 days (60 * 60 * 24 * 7)
  - `samesite`: lax
  - `httponly`: true

### Auth Middleware
- **Function**: `get_current_user()` in `app/auth.py`
- **Usage**: Reads token from `request.cookies.get("access_token")`
- **Behavior**: Returns `None` if no token or invalid token
- **Protected routes**: Use `require_auth()` decorator for protected pages

### Password Handling
- **Hashing**: bcrypt with 72-byte limit (truncates longer passwords)
- **Verification**: `verify_password()` compares plain vs hashed
- **Registration**: `register_user()` creates new users with hashed passwords

---

## 🗃️ Database Schema

### Tables

#### `users`
| Column | Type | Description |
|--------|------|-------------|
| id | Integer (PK) | Auto-incrementing ID |
| email | String(255) | Unique email address |
| username | String(100) | Unique username |
| hashed_password | String(255) | bcrypt hashed password |
| is_active | Boolean | Account active status |
| created_at | String(50) | ISO timestamp of creation |

#### `courses`
| Column | Type | Description |
|--------|------|-------------|
| id | Integer (PK) | Auto-incrementing ID |
| title | String(255) | Course title |
| slug | String(100) | URL-friendly identifier (unique) |
| description | Text | Course description |
| content | Text | Course content (Markdown) |
| icon | String(50) | Emoji code for course icon |
| order | Integer | Display order (default: 0) |
| is_premium | Boolean | Premium course flag (default: false) |

---

## 📚 Course Content Structure

### Sample Courses (auto-created on DB init)
1. **Python Programming** (`slug: python`)
   - Icon: 💻
   - Order: 1
   - Content: Markdown with headings (`#`, `##`, `###`) and bullet points

2. **More Courses** (`slug: more-courses`)
   - Icon: 📚
   - Order: 2

3. **Machine Learning** (`slug: machine-learning`)
   - Icon: 🧠
   - Order: 3

4. **Rust Programming** (`slug: rust`)
   - Icon: ⚙️
   - Order: 4

### Content Rendering
- **Template engine**: Inline HTML in FastAPI route functions (no separate templates)
- **Markdown processing**: Simple regex conversion in `/course/{slug}` route
- **Icons**: Map from `course.icon` to emoji codes in the UI

---

## 🎯 Routes & Pages

### Public Routes
- `GET /` - Home page with course listings
- `GET /login` - Login form
- `POST /login` - Process login (sets JWT cookie)
- `GET /register` - Registration form
- `POST /register` - Process registration
- `GET /logout` - Clear JWT cookie and redirect to home

### Protected Routes (require auth)
- `GET /courses` - List all courses for logged-in user
- `GET /course/{slug}` - View specific course content
- `GET /settings` - Account settings page
- `POST /settings/password` - Change password
- `POST /settings/delete` - Delete account

### Route Patterns
- All routes return HTML responses (FastAPI `HTMLResponse`)
- Authentication enforced via `get_current_user()` check
- Redirects to `/login` when unauthenticated

---

## 🔧 Configuration & Environment

### Hardcoded Values (change for production!)
```python
# app/database.py
SECRET_KEY = "your-secret-key-change-in-production"  # 🔴 Change this!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_URL = "sqlite:///./courses.db"
```

### Environment Requirements
- Python 3.11+ (virtual environment recommended)
- SQLite (built-in, no separate server needed)
- Internet connection for Tailwind CDN and Font Awesome

---

## 🐛 Testing & Debugging

### Test Files
- `test_auth_fix.py` - Authentication-related tests
- `test_e2e_login.py` - End-to-end login flow tests
- `debug_login.py` - Manual login debugging script
- `debug_token.py` - JWT token inspection/debugging

### Debug Commands
```bash
# Debug login flow
python debug_login.py

# Inspect JWT token
python debug_token.py <token>

# Run specific test
python -m pytest test_e2e_login.py -v
```

### Common Issues
1. **Database not initialized**: Run `python -c "from app.database import init_db; init_db()"`
2. **Port 8000 in use**: Change port in `run.sh` or kill existing process
3. **Token not set**: Verify login endpoint returns 302 redirect with Set-Cookie header
4. **SQLite lock errors**: Ensure no other process has the database open

---

## 📝 Code Style & Conventions

### Python Style
- **Framework**: FastAPI conventions
- **ORM**: SQLAlchemy declarative models
- **Auth**: JWT with python-jose
- **Passwords**: bcrypt via passlib

### Frontend Style
- **CSS**: Tailwind CDN (no build step)
- **Icons**: Font Awesome 6.4.0 CDN
- **JavaScript**: Inline in HTML templates (no separate JS files except `/static/register.js`)

### HTML Structure
- **Layout**: Tailwind CSS with dark theme (bg-gray-900)
- **Components**: Reusable HTML snippets in FastAPI route functions
- **Forms**: POST to route handlers with form data

### File Organization
- **Routes**: In `main.py` by URL path
- **Auth logic**: In `auth.py` module
- **Database models**: In `database.py`
- **Static assets**: In `app/static/` directory

---

## 🚨 Critical Warnings & Gotchas

### 🔴 Production Security Issues
1. **SECRET_KEY is hardcoded** - Change immediately for production!
2. **SQLite database** - Not suitable for multi-user production (consider PostgreSQL)
3. **No rate limiting** - Vulnerable to brute force attacks
4. **No CSRF protection** - Forms are vulnerable without CSRF tokens
5. **Password length limited to 72 bytes** - bcrypt limitation (enforced in `auth.py`)

### ⚠️ Development Quirks
1. **Database auto-creates** on first `init_db()` call
2. **Sample courses auto-populate** on first DB initialization
3. **Tailwind and Font Awesome load from CDN** - requires internet connection
4. **JWT tokens stored in HTTP-only cookies** - good for security, but harder to debug
5. **Virtual environment required** - dependencies won't work without venv

### 📊 Known Limitations
1. **No user progress tracking** - courses have no completion state
2. **No admin interface** - all users can view all courses
3. **No course editing** - courses are read-only after creation
4. **No email verification** - registration accepts any email
5. **No password reset** - users cannot recover lost passwords

---

## 🔄 Build & Deployment Flow

### Current Development Flow
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize database
python -c "from app.database import init_db; init_db()"

# 3. Start development server
./run.sh  # or: uvicorn app.main:app --reload

# 4. Access at http://localhost:8000
```

### For Production
1. Change `SECRET_KEY` in `app/database.py`
2. Replace SQLite with PostgreSQL/MySQL
3. Add rate limiting and CSRF protection
4. Set up proper email service for registration
5. Add HTTPS with valid certificate
6. Consider adding monitoring and logging

---

## 📚 References & Further Reading

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **JWT Best Practices**: https://datatracker.ietf.org/doc/html/rfc7519
- **bcrypt Documentation**: https://passlib.readthedocs.io/
- **Tailwind CSS**: https://tailwindcss.com/docs
- **python-jose**: https://python-jose.readthedocs.io/

---

## 💡 Agent Tips

### What NOT to Do
- ❌ Don't commit with hardcoded `SECRET_KEY`
- ❌ Don't use SQLite in production without backups
- ❌ Don't disable `--reload` in production
- ❌ Don't expose the database file
- ❌ Don't store plaintext passwords

### What TO Do
- ✅ Always initialize database before running tests
- ✅ Use virtual environment (`venv`)
- ✅ Check for existing `courses.db` before initializing
- ✅ Verify JWT cookie settings match your security requirements
- ✅ Test auth flow end-to-end (login → protected route → logout)

### Quick Verification Commands
```bash
# Check if server is running
curl -I http://localhost:8000

# Check database tables
sqlite3 courses.db ".tables"

# Check JWT token (after login)
# Inspect the access_token cookie value
```
