from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from passlib.context import CryptContext

# Database configuration
DATABASE_URL = "sqlite:///./courses.db"
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(String(50), default=None)


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    icon = Column(String(50), default="code")
    order = Column(Integer, default=0)
    is_premium = Column(Boolean, default=False)
    
    lessons = relationship("Lesson", back_populates="course", cascade="all, delete-orphan")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    lesson_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    slug = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    theory = Column(Text, nullable=False)
    order = Column(Integer, default=0)
    
    course = relationship("Course", back_populates="lessons")
    labs = relationship("Lab", back_populates="lesson", cascade="all, delete-orphan")


class Lab(Base):
    __tablename__ = "labs"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    starter_code = Column(Text, nullable=False)
    solution = Column(Text, nullable=False)
    hints = Column(Text, nullable=True)
    order = Column(Integer, default=0)
    
    lesson = relationship("Lesson", back_populates="labs")


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    lesson_id = Column(Integer, nullable=False, index=True)
    completed = Column(Boolean, default=False)
    completed_at = Column(String(50), nullable=True)
    lab_code = Column(Text, nullable=True)
    lab_completed = Column(Boolean, default=False)
    lab_completed_at = Column(String(50), nullable=True)


class Streak(Base):
    __tablename__ = "streaks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True, unique=True)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_activity_date = Column(String(50), nullable=True)


def init_db():
    """Initialize database with tables and sample courses."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Check if courses already exist
        existing = db.query(Course).first()
        if not existing:
            courses = [
                Course(
                    title="Python Programming",
                    slug="python",
                    description="Learn Python from scratch to advanced concepts. Master fundamentals, OOP, data structures, and build real projects.",
                    content="""# Welcome to Python Programming Course

## Course Overview
This comprehensive course will take you from Python basics to advanced concepts.

## Topics Covered
- Python Fundamentals (variables, data types, operators)
- Control Flow (if/else, loops, match statements)
- Functions and Modules
- Object-Oriented Programming
- Data Structures (lists, dictionaries, sets, tuples)
- File I/O and Error Handling
- Working with APIs
- Database connections

## Getting Started
Each module includes theory and hands-on exercises. By the end, you'll build complete applications.

## Prerequisites
- Basic computer skills
- No prior programming experience needed
""",
                    icon="code",
                    order=1
                ),
                Course(
                    title="More Courses",
                    slug="more-courses",
                    description="Explore additional programming courses and expand your skills with web development, APIs, and more.",
                    content="""# More Programming Courses

## Course Overview
Expand your programming knowledge with additional topics and technologies.

## Topics Covered
- Web Development Basics
- RESTful API Design
- Database Management
- Version Control with Git
- Testing Fundamentals
- Deployment Strategies
- Docker Basics
- CI/CD Pipelines

## Projects
Build a complete blog, todo app, and REST API.

## Prerequisites
- Basic Python knowledge recommended
""",
                    icon="book",
                    order=2
                ),
                Course(
                    title="Machine Learning",
                    slug="machine-learning",
                    description="Dive into ML algorithms, neural networks, and AI. Learn to build intelligent systems with Python.",
                    content="""# Machine Learning Course

## Course Overview
Master machine learning algorithms and build AI-powered applications.

## Topics Covered
- Introduction to ML
- Supervised Learning
- Unsupervised Learning
- Neural Networks
- Deep Learning Basics
- Computer Vision
- Natural Language Processing
- Model Training & Evaluation

## Tools You'll Learn
- NumPy, Pandas, Scikit-learn
- TensorFlow / PyTorch
- Matplotlib for visualization

## Prerequisites
- Python proficiency
- Basic math (linear algebra, calculus helpful)
""",
                    icon="brain",
                    order=3
                ),
                Course(
                    title="Rust Programming",
                    slug="rust",
                    description="Learn Rust - the systems programming language. Build fast, safe applications with memory safety.",
                    content="""# Rust Programming Course

## Course Overview
Master Rust programming for high-performance, memory-safe applications.

## Topics Covered
- Rust Fundamentals
- Ownership & Borrowing
- Structs and Enums
- Pattern Matching
- Error Handling
- Lifetimes
- Concurrency
- Building CLI Tools

## Why Rust?
- Memory safety without garbage collection
- Extreme performance
- Modern tooling (Cargo)
- Growing ecosystem

## Prerequisites
- Programming experience recommended
- Understanding of basic CS concepts
""",
                    icon="cpu",
                    order=4
                ),
            ]
            db.add_all(courses)
            db.commit()
            print("Database initialized with sample courses!")
    finally:
        db.close()


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()