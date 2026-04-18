from datetime import datetime
from fastapi import FastAPI, Request, Depends, HTTPException, status, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.database import get_db, Course, init_db, User
from app.auth import get_current_user, require_auth, login_user, logout_user, register_user

app = FastAPI(title="Course Platform")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.on_event("startup")
def startup():
    init_db()


@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    courses = db.query(Course).order_by(Course.order).all()
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Course Platform - Learn Programming</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-gray-900 text-gray-100 min-h-screen">
    <nav class="bg-gray-800 border-b border-gray-700">
        <div class="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
            <a href="/" class="text-2xl font-bold text-indigo-400">
                <i class="fas fa-code mr-2"></i>CourseHub
            </a>
            <div class="flex items-center gap-4">
                {"".join([f'<a href="/login" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-lg transition">Login</a>' + 
                          f'<a href="/register" class="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition">Sign Up</a>' if not user else 
                          f'<span class="text-gray-400">Hello, {user.username}</span>' + 
                          f'<a href="/courses" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-lg transition">My Courses</a>' + 
                          f'<a href="/logout" class="px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition">Logout</a>'])}
            </div>
        </div>
    </nav>
    
    <div class="max-w-6xl mx-auto px-4 py-12">
        <div class="text-center mb-12">
            <h1 class="text-5xl font-bold mb-4">Learn to <span class="text-indigo-400">Code</span></h1>
            <p class="text-xl text-gray-400 max-w-2xl mx-auto">
                Master programming with our comprehensive courses. Python, Machine Learning, Rust, and more!
            </p>
        </div>
        
        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {"".join([f'''
            <div class="bg-gray-800 rounded-xl p-6 border border-gray-700 hover:border-indigo-500 transition duration-300">
                <div class="text-4xl mb-4">
                    {"".join([{"code": "💻", "book": "📚", "brain": "🧠", "cpu": "⚙️"}.get(course.icon, "📖")])}
                </div>
                <h3 class="text-xl font-bold mb-2">{course.title}</h3>
                <p class="text-gray-400 text-sm mb-4">{course.description[:100]}...</p>
                <a href="/courses" class="text-indigo-400 hover:text-indigo-300">
                    View Course <i class="fas fa-arrow-right ml-1"></i>
                </a>
            </div>''' for course in courses])}
        </div>
        
        <div class="mt-16 text-center">
            <div class="bg-gray-800 rounded-xl p-8 border border-gray-700 max-w-2xl mx-auto">
                <h2 class="text-2xl font-bold mb-4">Get Started Today</h2>
                <p class="text-gray-400 mb-6">Create an account to access all courses and track your progress.</p>
                <a href="/register" class="inline-block px-6 py-3 bg-indigo-600 hover:bg-indigo-700 rounded-lg transition text-lg">
                    Create Free Account
                </a>
            </div>
        </div>
    </div>
    
    <footer class="border-t border-gray-800 mt-12 py-8">
        <div class="max-w-6xl mx-auto px-4 text-center text-gray-500">
            <p>&copy; 2026 CourseHub. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>"""
    return html


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, error: str = None):
    user = getattr(request.state, "user", None)
    if user:
        return RedirectResponse("/courses", status_code=302)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Course Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-gray-900 text-gray-100 min-h-screen flex items-center justify-center">
    <div class="w-full max-w-md">
        <div class="bg-gray-800 rounded-xl p-8 border border-gray-700">
            <a href="/" class="text-2xl font-bold text-indigo-400 mb-8 block text-center">
                <i class="fas fa-code mr-2"></i>CourseHub
            </a>
            
            <h1 class="text-2xl font-bold mb-6 text-center">Welcome Back</h1>
            
            {"".join([f'<div class="bg-red-900/50 border border-red-700 text-red-200 px-4 py-3 rounded-lg mb-4">{error}</div>' if error else ""])}
            
            <form method="post" action="/login">
                <div class="mb-4">
                    <label class="block text-gray-400 mb-2">Username</label>
                    <input type="text" name="username" required
                        class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 focus:border-indigo-500 focus:outline-none">
                </div>
                
                <div class="mb-6">
                    <label class="block text-gray-400 mb-2">Password</label>
                    <input type="password" name="password" required
                        class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 focus:border-indigo-500 focus:outline-none">
                </div>
                
                <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-700 py-3 rounded-lg font-bold transition">
                    Login
                </button>
            </form>
            
            <p class="text-center text-gray-400 mt-6">
                Don't have an account? 
                <a href="/register" class="text-indigo-400 hover:text-indigo-300">Sign up</a>
            </p>
        </div>
    </div>
</body>
</html>"""
    return html


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request, error: str = None):
    from app.auth import generate_captcha
    user = getattr(request.state, "user", None)
    if user:
        return RedirectResponse("/courses", status_code=302)
    
    captcha_question, captcha_signature = generate_captcha()
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign Up - Course Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-gray-900 text-gray-100 min-h-screen flex items-center justify-center">
    <div class="w-full max-w-md">
        <div class="bg-gray-800 rounded-xl p-8 border border-gray-700">
            <a href="/" class="text-2xl font-bold text-indigo-400 mb-8 block text-center">
                <i class="fas fa-code mr-2"></i>CourseHub
            </a>
            
            <h1 class="text-2xl font-bold mb-6 text-center">Create Account</h1>
            
            {"".join([f'<div class="bg-red-900/50 border border-red-700 text-red-200 px-4 py-3 rounded-lg mb-4">{error}</div>' if error else ""])}
            
            <form method="post" action="/register" id="registerForm">
                <div class="mb-4">
                    <label class="block text-gray-400 mb-2">Email</label>
                    <input type="email" name="email" required
                        class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 focus:border-indigo-500 focus:outline-none">
                </div>
                
                <div class="mb-4">
                    <label class="block text-gray-400 mb-2">Username</label>
                    <input type="text" name="username" required minlength=3
                        class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 focus:border-indigo-500 focus:outline-none">
                </div>
                
                <div class="mb-2">
                    <label class="block text-gray-400 mb-2">Password</label>
                    <input type="password" name="password" id="passwordField" required minlength=6
                        class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 focus:border-indigo-500 focus:outline-none">
                </div>
                
                <div class="mb-4">
                    <div class="h-1.5 bg-gray-700 rounded-full overflow-hidden">
                        <div id="strengthBar" class="h-full transition-all duration-300" style="width: 0%25"></div>
                    </div>
                    <div class="flex justify-between text-xs mt-1">
                        <span id="strengthText" class="text-gray-500">Password strength</span>
                        <span id="charCount" class="text-gray-500">0 chars</span>
                    </div>
                </div>
                
                <div class="mb-4 text-sm space-y-1">
                    <div class="flex items-center gap-2">
                        <span id="req-length" class="text-gray-500"><i class="fas fa-circle text-xs"></i> 8+ characters</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span id="req-lower" class="text-gray-500"><i class="fas fa-circle text-xs"></i> Lowercase</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span id="req-upper" class="text-gray-500"><i class="fas fa-circle text-xs"></i> Uppercase</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span id="req-number" class="text-gray-500"><i class="fas fa-circle text-xs"></i> Number</span>
                    </div>
                </div>
                
                <div class="mb-4">
                    <label class="block text-gray-400 mb-2">Security Check</label>
                    <div class="text-lg mb-2">{captcha_question}</div>
                    <input type="number" name="captcha_answer" required
                        class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 focus:border-indigo-500 focus:outline-none">
                    <input type="hidden" name="captcha_signature" value="{captcha_signature}">
                </div>
                
                <button type="submit" id="submitBtn" class="w-full bg-indigo-600 hover:bg-indigo-700 py-3 rounded-lg font-bold transition disabled:opacity-50 disabled:cursor-not-allowed">
                    Create Account
                </button>
            </form>
            
            <p class="text-center text-gray-400 mt-6">
                Already have an account? 
                <a href="/login" class="text-indigo-400 hover:text-indigo-300">Login</a>
            </p>
        </div>
    </div>
    
    <script src="/static/register.js"></script>
</body>
</html>"""
    return html


@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        html = login_page(request, error="Invalid username or password")
        return HTMLResponse(content=html, status_code=200)
    
    from app.auth import verify_password
    if not verify_password(password, user.hashed_password):
        html = login_page(request, error="Invalid username or password")
        return HTMLResponse(content=html, status_code=200)
    
    from app.auth import create_access_token
    token = create_access_token(data={"sub": user.username})
    
    response = RedirectResponse(url="/courses", status_code=302)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=60 * 60 * 24 * 7,
        samesite="lax"
    )
    return response


@app.post("/register")
async def register(
    request: Request,
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    captcha_answer: str = Form(...),
    captcha_signature: str = Form(...),
    db: Session = Depends(get_db)
):
    from app.auth import verify_captcha
    if not verify_captcha(captcha_answer, captcha_signature):
        html = register_page(request, error="Incorrect answer. Please try again.")
        return HTMLResponse(content=html, status_code=200)
    
    existing = db.query(User).filter(
        (User.email == email) | (User.username == username)
    ).first()
    
    if existing:
        html = register_page(request, error="Email or username already exists")
        return HTMLResponse(content=html, status_code=200)
    
    from app.auth import get_password_hash
    hashed_password = get_password_hash(password)
    
    user = User(
        email=email,
        username=username,
        hashed_password=hashed_password,
        is_active=True,
        created_at=datetime.utcnow().isoformat()
    )
    db.add(user)
    db.commit()
    
    return RedirectResponse(url="/login?registered=true", status_code=302)


@app.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("access_token")
    return response


@app.get("/courses", response_class=HTMLResponse)
def courses_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=302)
    
    courses = db.query(Course).order_by(Course.order).all()
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Courses - Course Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-gray-900 text-gray-100 min-h-screen">
    <nav class="bg-gray-800 border-b border-gray-700">
        <div class="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
            <a href="/" class="text-2xl font-bold text-indigo-400">
                <i class="fas fa-code mr-2"></i>CourseHub
            </a>
            <div class="flex items-center gap-4">
                <a href="/settings" class="text-gray-400 hover:text-white">Settings</a>
                <span class="text-gray-400">Hello, {user.username}</span>
                <a href="/logout" class="px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition">Logout</a>
            </div>
        </div>
    </nav>
    
    <div class="max-w-6xl mx-auto px-4 py-12">
        <h1 class="text-3xl font-bold mb-8">My Courses</h1>
        
        <div class="grid md:grid-cols-2 gap-6">
            {"".join([f'''
            <a href="/course/{course.slug}" class="bg-gray-800 rounded-xl p-6 border border-gray-700 hover:border-indigo-500 transition duration-300 block">
                <div class="flex items-start gap-4">
                    <div class="text-4xl">
                        {"".join([{"code": "💻", "book": "📚", "brain": "🧠", "cpu": "⚙️"}.get(course.icon, "📖")])}
                    </div>
                    <div>
                        <h3 class="text-xl font-bold mb-2">{course.title}</h3>
                        <p class="text-gray-400">{course.description}</p>
                        <span class="inline-block mt-4 text-indigo-400">
                            Start Learning <i class="fas fa-arrow-right ml-1"></i>
                        </span>
                    </div>
                </div>
            </a>''' for course in courses])}
        </div>
    </div>
</body>
</html>"""
    return html


@app.get("/course/{slug}", response_class=HTMLResponse)
def course_detail(slug: str, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=302)
    
    course = db.query(Course).filter(Course.slug == slug).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    import re
    content_html = re.sub(r'^# (.+)$', r'<h1 class="text-3xl font-bold mb-6">\1</h1>', course.content, flags=re.MULTILINE)
    content_html = re.sub(r'^## (.+)$', r'<h2 class="text-2xl font-bold mb-4 mt-8">\1</h2>', content_html, flags=re.MULTILINE)
    content_html = re.sub(r'^### (.+)$', r'<h3 class="text-xl font-bold mb-3 mt-6">\1</h3>', content_html, flags=re.MULTILINE)
    content_html = re.sub(r'^[-*] (.+)$', r'<li class="ml-4 mb-2">\1</li>', content_html, flags=re.MULTILINE)
    content_html = re.sub(r'^(.+)$', r'<p class="mb-4 text-gray-300">\1</p>', content_html, flags=re.MULTILINE)
    content_html = content_html.replace("\n\n", "</p>\n<p class=\"mb-4 text-gray-300\">")
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{course.title} - Course Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-gray-900 text-gray-100 min-h-screen">
    <nav class="bg-gray-800 border-b border-gray-700">
        <div class="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
            <a href="/" class="text-2xl font-bold text-indigo-400">
                <i class="fas fa-code mr-2"></i>CourseHub
            </a>
            <div class="flex items-center gap-4">
                <a href="/courses" class="text-gray-400 hover:text-white">Courses</a>
                <a href="/settings" class="text-gray-400 hover:text-white">Settings</a>
                <a href="/logout" class="px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition">Logout</a>
            </div>
        </div>
    </nav>
    
    <div class="max-w-4xl mx-auto px-4 py-12">
        <a href="/courses" class="text-gray-400 hover:text-white mb-6 inline-block">
            <i class="fas fa-arrow-left mr-2"></i>Back to Courses
        </a>
        
        <div class="bg-gray-800 rounded-xl p-8 border border-gray-700">
            <div class="flex items-center gap-4 mb-6">
                <div class="text-5xl">
                    {"".join([{"code": "💻", "book": "📚", "brain": "🧠", "cpu": "⚙️"}.get(course.icon, "📖")])}
                </div>
                <div>
                    <h1 class="text-3xl font-bold">{course.title}</h1>
                    <p class="text-gray-400">{course.description[:100]}...</p>
                </div>
            </div>
            
            <div class="prose prose-invert max-w-none">
                {content_html}
            </div>
        </div>
    </div>
</body>
</html>"""
    return html


@app.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=302)
    
    success = getattr(request, "success", None)
    error = getattr(request, "error", None)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Account Settings - Course Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-gray-900 text-gray-100 min-h-screen">
    <nav class="bg-gray-800 border-b border-gray-700">
        <div class="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
            <a href="/" class="text-2xl font-bold text-indigo-400">
                <i class="fas fa-code mr-2"></i>CourseHub
            </a>
            <div class="flex items-center gap-4">
                <a href="/courses" class="text-gray-400 hover:text-white">Courses</a>
                <span class="text-gray-400">Hello, {user.username}</span>
                <a href="/logout" class="px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition">Logout</a>
            </div>
        </div>
    </nav>
    
    <div class="max-w-2xl mx-auto px-4 py-12">
        <h1 class="text-3xl font-bold mb-8">Account Settings</h1>
        
        {"".join([f'<div class="bg-green-900/50 border border-green-700 text-green-200 px-4 py-3 rounded-lg mb-4">{success}</div>' if success else ""])}
        {"".join([f'<div class="bg-red-900/50 border border-red-700 text-red-200 px-4 py-3 rounded-lg mb-4">{error}</div>' if error else ""])}
        
        <div class="bg-gray-800 rounded-xl p-6 border border-gray-700 mb-6">
            <h2 class="text-xl font-bold mb-4">Profile Information</h2>
            <div class="space-y-4">
                <div>
                    <label class="block text-gray-400 mb-2">Email</label>
                    <div class="bg-gray-700 rounded-lg px-4 py-3 text-gray-300">{user.email}</div>
                </div>
                <div>
                    <label class="block text-gray-400 mb-2">Username</label>
                    <div class="bg-gray-700 rounded-lg px-4 py-3 text-gray-300">{user.username}</div>
                </div>
                <div>
                    <label class="block text-gray-400 mb-2">Member Since</label>
                    <div class="bg-gray-700 rounded-lg px-4 py-3 text-gray-300">{user.created_at or 'N/A'}</div>
                </div>
            </div>
        </div>
        
        <div class="bg-gray-800 rounded-xl p-6 border border-gray-700 mb-6">
            <h2 class="text-xl font-bold mb-4">Change Password</h2>
            <form method="post" action="/settings/password">
                <div class="mb-4">
                    <label class="block text-gray-400 mb-2">Current Password</label>
                    <input type="password" name="current_password" required
                        class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 focus:border-indigo-500 focus:outline-none">
                </div>
                <div class="mb-4">
                    <label class="block text-gray-400 mb-2">New Password</label>
                    <input type="password" name="new_password" id="newPassword" required minlength=8
                        class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 focus:border-indigo-500 focus:outline-none">
                </div>
                <div class="mb-4">
                    <label class="block text-gray-400 mb-2">Confirm New Password</label>
                    <input type="password" name="confirm_password" required
                        class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 focus:border-indigo-500 focus:outline-none">
                </div>
                <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-700 py-3 rounded-lg font-bold transition">
                    Update Password
                </button>
            </form>
        </div>
        
        <div class="bg-gray-800 rounded-xl p-6 border border-gray-700">
            <h2 class="text-xl font-bold mb-4 text-red-400">Danger Zone</h2>
            <p class="text-gray-400 mb-4">Once you delete your account, there is no going back.</p>
            <form method="post" action="/settings/delete" onsubmit="return confirm('Are you sure? This cannot be undone.');">
                <button type="submit" class="w-full bg-red-600 hover:bg-red-700 py-3 rounded-lg font-bold transition">
                    Delete Account
                </button>
            </form>
        </div>
    </div>
</body>
</html>"""
    return html


@app.post("/settings/password")
def update_password(
    request: Request,
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=302)
    
    from app.auth import verify_password, get_password_hash
    
    if not verify_password(current_password, user.hashed_password):
        request.success = None
        request.error = "Current password is incorrect"
        return settings_page(request, db)
    
    if new_password != confirm_password:
        request.success = None
        request.error = "New passwords do not match"
        return settings_page(request, db)
    
    if len(new_password) < 8:
        request.success = None
        request.error = "Password must be at least 8 characters"
        return settings_page(request, db)
    
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    
    request.error = None
    request.success = "Password updated successfully!"
    return settings_page(request, db)


@app.post("/settings/delete")
def delete_account(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=302)
    
    db.delete(user)
    db.commit()
    
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("access_token")
    return response