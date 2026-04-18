from datetime import datetime, timedelta
from typing import Optional
import bcrypt
import random
import hashlib
import hmac

from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.database import get_db, User, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def generate_captcha():
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    op = random.choice(['+', '-', '*'])
    if op == '+':
        answer = a + b
        question = f"What is {a} + {b}?"
    elif op == '-':
        if a < b:
            a, b = b, a
        answer = a - b
        question = f"What is {a} - {b}?"
    else:
        a = random.randint(2, 10)
        b = random.randint(2, 5)
        answer = a * b
        question = f"What is {a} × {b}?"
    
    signature = hmac.new(SECRET_KEY.encode(), str(answer).encode(), hashlib.sha256).hexdigest()
    return question, signature


def verify_captcha(answer: str, signature: str) -> bool:
    if not answer or not signature:
        return False
    try:
        expected = hmac.new(SECRET_KEY.encode(), answer.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)
    except:
        return False


def verify_password(plain_password: str, hashed_password: str) -> bool:
    pw = plain_password.encode('utf-8')
    if len(pw) > 72:
        pw = pw[:72]
    hashed = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pw, hashed)


def get_password_hash(password: str) -> str:
    if len(password.encode('utf-8')) > 72:
        password = password[:72]
    pw = password.encode('utf-8')
    return bcrypt.hashpw(pw, bcrypt.gensalt()).decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": int(expire.timestamp())})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_persistent_token() -> str:
    import secrets
    return secrets.token_urlsafe(32)


def get_current_user(request: Request, db: Session) -> Optional[User]:
    token = request.cookies.get("access_token")
    if not token:
        persistent_token = request.cookies.get("persistent_token")
        if persistent_token:
            user = db.query(User).filter(User.persistent_token == persistent_token).first()
            if user:
                expires = user.persistent_token_expires
                if expires and datetime.fromisoformat(expires) > datetime.utcnow():
                    return user
        return None
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
    except JWTError:
        return None
    
    user = db.query(User).filter(User.username == username).first()
    return user


def require_auth(request: Request, db: Session) -> User:
    user = get_current_user(request, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            headers={"Location": "/login"}
        )
    return user


def login_user(request: Request, username: str, password: str, db: Session) -> Optional[User]:
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    
    token = create_access_token(data={"sub": user.username})
    response = RedirectResponse(url="/courses", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=60 * 60 * 24 * 7,
        samesite="lax"
    )
    request.state.response = response
    return user


def logout_user(request: Request):
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response


def register_user(email: str, username: str, password: str, db: Session) -> User:
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
    db.refresh(user)
    return user