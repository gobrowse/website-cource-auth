#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/devgobrowse/code/website-cource-auth')

from app.database import SessionLocal, Course, Lesson, Lab

db = SessionLocal()

python_topics = [
    ("Hello World and Setup", "hello-world", "Learn Python basics", "print('Hello World')", "print('Hello World')", 1),
    ("Variables and Data Types", "variables-data-types", "Understanding variables", "x = 5", "x = 5\nprint(x)", 2),
    ("Numbers and Strings", "numbers-strings", "Working with numbers", "x = 10", "x = 10\nprint(x)", 3),
    ("Boolean and None", "boolean-none", "Truth values", "True", "x = True\nprint(x)", 4),
    ("Lists Basics", "lists-basics", "List intro", "[1,2,3]", "l = [1,2,3]\nprint(l)", 5),
    ("Lists Operations", "lists-operations", "List methods", "l.append(1)", "l = [1,2]\nl.append(3)\nprint(l)", 6),
    ("Tuples", "tuples", "Immutable sequences", "(1,2)", "t = (1,2)\nprint(t)", 7),
    ("Dictionaries Basics", "dict-basics", "Key-value pairs", "{'a':1}", "d = {'a':1}\nprint(d)", 8),
    ("Dictionary Operations", "dict-operations", "Dict methods", "d.keys()", "d = {'a':1}\nprint(d.keys())", 9),
    ("Sets", "sets", "Unique elements", "{1,2,3}", "s = {1,2,3}\nprint(s)", 10),
    ("If-Else", "if-else", "Conditional logic", "if x > 5:", "x = 10\nif x > 5:\n    print('big')", 11),
    ("Elif", "elif", "Multiple conditions", "elif x > 5:", "x = 7\nif x > 10:\n    print('big')\nelif x > 5:\n    print('med')", 12),
    ("For Loops", "for-loops", "Iteration", "for i in range(5):", "for i in range(5):\n    print(i)", 13),
    ("While Loops", "while-loops", "Condition loops", "while x < 5:", "x = 0\nwhile x < 3:\n    print(x)\n    x += 1", 14),
    ("Loop Control", "loop-control", "break/continue", "break", "for i in range(5):\n    if i == 3:\n        break\n    print(i)", 15),
    ("List Comprehensions", "list-comprehensions", "Concise lists", "[x for x in l]", "[x**2 for x in range(5)]", 16),
    ("Functions Basics", "functions-basics", "Reusable code", "def f():", "def greet():\n    print('Hi!')\ngreet()", 17),
    ("Function Parameters", "function-parameters", "Input functions", "def f(x):", "def greet(name):\n    print(f'Hi {name}!')\ngreet('Alice')", 18),
    ("Return Values", "return-values", "Output from functions", "return x", "def add(a,b):\n    return a+b\nprint(add(3,4))", 19),
    ("Function Scope", "scope", "Variable visibility", "global x", "x = 10\ndef f():\n    global x\n    x = 5\nf()\nprint(x)", 20),
    ("Args and Kwargs", "args-kwargs", "Flexible args", "*args", "def f(*args, **kwargs):\n    print(args, kwargs)\nf(1,2,a=3)", 21),
    ("Lambda Functions", "lambda", "Anonymous functions", "lambda x: x", "square = lambda x: x**2\nprint(square(5))", 22),
    ("Module Import", "module-import", "Using modules", "import math", "import math\nprint(math.pi)", 23),
    ("Modules Creating", "modules-creating", "Creating modules", "def f():", "def greet(): return 'Hi'\n# import as greet", 24),
    ("File Reading", "file-reading", "Read files", "open('f')", "with open('f.txt') as f:\n    print(f.read())", 25),
    ("File Writing", "file-writing", "Write files", "open('w')", "with open('f.txt','w') as f:\n    f.write('Hi')", 26),
    ("Try Except", "try-except", "Error handling", "try/except", "try:\n    x = 1/0\nexcept:\n    print('error')", 27),
    ("Finally", "finally", "Cleanup code", "finally", "try:\n    print(1)\nexcept:\n    print('e')\nfinally:\n    print('done')", 28),
    ("Classes Basics", "classes-basics", "OOP intro", "class Dog:", "class Dog:\n    def __init__(self,name):\n        self.name = name\nd = Dog('Rex')", 29),
    ("Class Methods", "class-methods", "Methods in classes", "def bark(self)", "class Dog:\n    def bark(self):\n        return 'Woof'\nprint(Dog().bark())", 30),
    ("Inheritance", "inheritance", "Inherit classes", "class C(P):", "class Animal:\n    def speak(self): return ''\nclass Dog(Animal):\n    def speak(self): return 'Woof'", 31),
    ("Dunder Methods", "dunder-methods", "Special methods", "__str__", "class P:\n    def __str__(self): return 'P'", 32),
    ("Encapsulation", "encapsulation", "Data hiding", "self._x", "class A:\n    def __init__(self):\n        self._x = 0", 33),
    ("Polymorphism", "polymorphism", "Same interface", "def f(obj):", "def f(x): print(x.speak())\nclass D: def speak(self): return 'M'\nf(D())", 34),
    ("Decorators", "decorators", "Modify behavior", "@dec", "def dec(f):\n    def w():\n        f()\n    return w", 35),
    ("Generators", "generators", "Lazy iteration", "yield", "def gen():\n    for i in range(3):\n        yield i\nprint(list(gen()))", 36),
    ("Iterators", "iterators", "Custom iteration", "__iter__", "class C:\n    def __iter__(self): return self\nprint(iter(C()))", 37),
    ("Counter", "counter", "Counting", "Counter", "from collections import Counter\nprint(Counter('aab'))", 38),
    ("DefaultDict", "defaultdict", "Default dict", "defaultdict", "from collections import defaultdict\nd = defaultdict(int)\nprint(d['a'])", 39),
    ("Regex Basics", "regex-basics", "Pattern matching", "import re", "import re\nprint(re.search(r'\\d+','a123'))", 40),
    ("Regex Patterns", "regex-patterns", "Complex patterns", "r'\\d+'", "import re\nprint(re.findall(r'\\d+','a1b2'))", 41),
    ("Virtual Env", "venv", "Isolated envs", "python -m venv", "python -m venv venv", 42),
    ("PIP", "pip", "Package manager", "pip install", "pip install requests", 43),
    ("Debugging", "debugging", "Find bugs", "pdb.set_trace()", "import pdb; pdb.set_trace()", 44),
    ("Unit Testing", "unittest", "Test code", "assert", "assert 1+1==2", 45),
    ("Logging", "logging", "Log events", "logging.info", "import logging\nlogging.basicConfig(level=10)", 46),
    ("Datetime", "datetime", "Date/time", "datetime.now", "from datetime import datetime\nprint(datetime.now())", 47),
    ("JSON", "json", "JSON handling", "json.dumps", "import json\nprint(json.dumps({'a':1}))", 48),
    ("HTTP Requests", "http-requests", "Web requests", "requests.get", "import requests\nr = requests.get('http://example.com')", 49),
    ("FastAPI", "fastapi", "Build APIs", "FastAPI", "from fastapi import FastAPI\napp = FastAPI()", 50),
]

for i, title, slug, starter, solution, num in python_topics:
    lesson = Lesson(course_id=1, lesson_number=num, title=title, slug=slug,
                  description=f"Learn {title}", content=starter, theory=starter, order=num)
    db.add(lesson)
    db.flush()
    lab = Lab(lesson_id=lesson.id, title=f"Practice {title}", description=f"Practice {title}",
            starter_code=starter, solution=solution, hints="Try the code", order=num)
    db.add(lab)


rust_topics = [
    ("Why Rust?", "why-rust", "Rust benefits", "fn main(){ println!(\"Hi\"); }", "fn main(){ println!(\"Hi\"); }", 1),
    ("Installation", "rust-installation", "Install Rust", "rustc --version", "rustc --version", 2),
    ("Hello World", "rust-hello-world", "First program", "fn main(){ println!(\"Hi\"); }", "fn main(){ println!(\"Hello\"); }", 3),
    ("Variables", "rust-variables", "Variables", "let x = 5;", "let mut x = 5; x = 6; println!(\"{}\",x);", 4),
    ("Data Types", "rust-data-types", "Types", "let x: i32 = 5;", "let x: i32 = 42; println!(\"{}\",x);", 5),
    ("Operators", "rust-operators", "Math", "10 + 3", "let a = 10; let b = 3; println!(\"{}\",a+b);", 6),
    ("Ownership", "ownership", "Memory", "let s1 = String::from(\"hi\");", "let s = String::from(\"hi\"); println!(\"{}\",s);", 7),
    ("Borrowing", "borrowing", "References", "fn f(s: &str)", "fn f(s: &str){} fn main(){ f(\"hi\"); }", 8),
    ("References", "references", "Reference types", "let r = &x;", "let x = 5; let r = &x; println!(\"{}\",r);", 9),
    ("Lifetimes", "lifetimes", "Lifetime syntax", "fn f<'a>(x: &'a str)", "fn f<'a>(x: &'a str) -> &'a str { x }", 10),
    ("Structs", "structs", "Custom types", "struct P{ name: String }", "struct P{ name: String } fn main(){ let p = P{ name: String::from(\"A\") }; }", 11),
    ("Impl Blocks", "impl-blocks", "Methods", "impl Dog{ fn new() }", "struct D; impl D{ fn new() -> Self{ D } }", 12),
    ("Methods", "methods", "Methods", "fn greet(&self)", "struct D; impl D{ fn g(&self){} }", 13),
    ("Enums", "enums", "Custom types", "enum C{ A, B }", "enum C{ A, B } fn main(){ let c = C::A; }", 14),
    ("Match", "match", "Pattern match", "match x{ 1=> }", "let x = 1; match x{ 1=>println!(\"1\"),_=>println!(\"?\"),}", 15),
    ("Pattern Matching", "pattern-matching", "Patterns", "(x,y)", "let p=(1,2); let (a,b)=p;", 16),
    ("Option Result", "option-result", "Error types", "Option<i32>", "let x: Option<i32> = Some(5);", 17),
    ("Error Handling", "error-handling", "Handle errors", ".unwrap()", "let x = Some(5).unwrap();", 18),
    ("Collections Vec", "collections-vec", "Dynamic arrays", "Vec::new()", "let mut v = vec![1,2,3]; v.push(4);", 19),
    ("Collections String", "collections-string", "Text", "String::from", "let s = String::from(\"hi\");", 20),
    ("Collections HashMap", "collections-hashmap", "Hash map", "HashMap::new()", "use std::collections::HashMap; let m = HashMap::new();", 21),
    ("Control Flow", "control-flow", "Conditionals", "if x > 5{}", "let x = 10; if x > 5{ println!(\"big\"); }", 22),
    ("Loops", "loops", "Iteration", "loop{ break }", "let mut i = 0; loop{ i+=1; if i==3{break;} }", 23),
    ("Functions", "functions", "Functions", "fn add(a:i32,b:i32)", "fn add(a:i32,b:i32)->i32{a+b} fn main(){ println!(\"{}\",add(3,4)); }", 24),
    ("Closures", "closures", "Anonymous", "|x| x+1", "let add = |a:i32,b:i32| a+b; println!(\"{}\",add(3,4));", 25),
    ("Iterators", "iterators", "Iterators", "iter()", "let v = vec![1,2,3]; for i in &v{ println!(\"{}\",i); }", 26),
    ("Modules", "modules", "Organization", "mod m{ pub fn f() }", "mod m{ pub fn f(){} } use m::f;", 27),
    ("Crates.io", "crates", "Packages", "cargo add", "cargo add serde", 28),
    ("Testing", "testing", "Tests", "#[test]", "#[test] fn t(){ assert_eq!(1,1); }", 29),
    ("Benchmarking", "benchmarking", "Perf", "cargo bench", "cargo bench", 30),
    ("Unsafe Rust", "unsafe-rust", "Unsafe", "unsafe{ }", "unsafe{ let p = &*std::ptr::null(); }", 31),
    ("Concurrency", "concurrency", "Parallel", "thread::spawn", "use std::thread; thread::spawn(||{println!(\"hi\");});", 32),
    ("Threads", "threads", "Threads", "thread::spawn", "use std::thread; let h = thread::spawn(||{}); h.join();", 33),
    ("Channels", "channels", "Message pass", "mpsc::channel", "use std::sync::mpsc; let (t,r)=mpsc::channel();", 34),
    ("Mutex", "mutex", "Locks", "Mutex::new", "use std::sync::Mutex; let m = Mutex::new(0);", 35),
    ("Async Basics", "async-basics", "Async", "async fn", "async fn f(){} fn main(){ }", 36),
    ("tokio", "tokio", "Async runtime", "tokio::main", "#[tokio::main] async fn main(){}", 37),
    ("Web Server", "web-server", "Server", "actix_web", "#[actix_web::main] async fn main(){}", 38),
    ("REST API", "rest-api", "API", "HttpResponse", "HttpResponse::Ok().json()", 39),
    ("Database rusqlite", "rusqlite", "SQLite", "rusqlite", "use rusqlite::Connection; let c = Connection::open(\"db\");", 40),
    ("Error Best Practices", "error-practices", "Errors", "thiserror", "use thiserror::Error; #[derive(Error)] pub enum E{}", 41),
    ("Cargo", "cargo", "Build tool", "cargo new", "cargo new myproject && cd myproject && cargo run", 42),
    ("Documentation", "documentation", "Docs", "///", "/// Doc comment pub fn f(){}", 43),
    ("Attribute Macros", "attribute-macros", "Attributes", "#[derive]", "#[derive(Debug)] struct A;", 44),
    ("Derive Macros", "derive-macros", "Generated", "Clone, Copy", "#[derive(Clone, Copy)] struct A;", 45),
    ("Procedural Macros", "proc-macros", "Macros", "macro_rules!", "macro_rules! hi{ ()=>{ println!(\"hi\"); } } hi!();", 46),
    ("FFI", "ffi", "Foreign interop", "extern C", "extern \"C\"{ fn abs(n:c_int)->c_int; }", 47),
    ("C Interop", "c-interop", "C interop", "bindgen", "bindgen cli.rs > lib.rs", 48),
    ("WASM", "wasm", "WebAssembly", "wasm-pack", "cargo install wasm-pack", 49),
    ("CLI Tools", "cli-tools", "CLI apps", "clap", "use clap::{App, Arg}; App::new(\"app\").get_matches();", 50),
]

for i, title, slug, starter, solution, num in rust_topics:
    lesson = Lesson(course_id=4, lesson_number=num, title=title, slug=slug,
                  description=f"Learn {title}", content=starter, theory=starter, order=num)
    db.add(lesson)
    db.flush()
    lab = Lab(lesson_id=lesson.id, title=f"Practice {title}", description=f"Practice {title}",
            starter_code=starter, solution=solution, hints="Try it", order=num)
    db.add(lab)


ml_topics = [
    ("What is ML?", "what-is-ml", "Intro", "print('ML')", "print('ML')", 1),
    ("Types of ML", "types-of-ml", "Categories", "supervised, unsupervised", "supervised unsupervised reinforcement", 2),
    ("Linear Regression", "linear-regression", "Regression", "sklearn.linear_model.LinearRegression", "from sklearn.linear_model import LinearRegression", 3),
    ("Gradient Descent", "gradient-descent", "Optimization", "minimize loss", "minimize loss", 4),
    ("Multiple Regression", "multiple-regression", "Many features", "multiple features", "multiple features", 5),
    ("Polynomial Regression", "polynomial-regression", "Curves", "PolynomialFeatures", "PolynomialFeatures", 6),
    ("Logistic Regression", "logistic-regression", "Classification", "sklearn.linear_model.LogisticRegression", "from sklearn.linear_model import LogisticRegression", 7),
    ("Decision Trees", "decision-trees", "Trees", "sklearn.tree.DecisionTreeClassifier", "from sklearn.tree import DecisionTreeClassifier", 8),
    ("Random Forests", "random-forests", "Ensembles", "RandomForestClassifier", "from sklearn.ensemble import RandomForestClassifier", 9),
    ("Gradient Boosting", "gradient-boosting", "Boosting", "GradientBoosting", "from sklearn.ensemble import GradientBoostingClassifier", 10),
    ("Support Vector Machines", "svm", "SVM", "SVC", "from sklearn.svm import SVC", 11),
    ("K-Nearest Neighbors", "knn", "KNN", "KNeighborsClassifier", "from sklearn.neighbors import KNeighborsClassifier", 12),
    ("Naive Bayes", "naive-bayes", "Bayes", "GaussianNB", "from sklearn.naive_bayes import GaussianNB", 13),
    ("K-Means Clustering", "kmeans", "K-Means", "KMeans", "from sklearn.cluster import KMeans", 14),
    ("Hierarchical Clustering", "hierarchical", "Clustering", "AgglomerativeClustering", "from sklearn.cluster import AgglomerativeClustering", 15),
    ("DBSCAN", "dbscan", "Density", "DBSCAN", "from sklearn.cluster import DBSCAN", 16),
    ("Principal Component Analysis", "pca", "PCA", "PCA", "from sklearn.decomposition import PCA", 17),
    ("SVD", "svd", "SVD", "TruncatedSVD", "from sklearn.decomposition import TruncatedSVD", 18),
    ("Feature Scaling", "feature-scaling", "Scaling", "StandardScaler", "from sklearn.preprocessing import StandardScaler", 19),
    ("Feature Selection", "feature-selection", "Selection", "SelectKBest", "from sklearn.feature_selection import SelectKBest", 20),
    ("Cross-Validation", "cross-validation", "CV", "cross_val_score", "from sklearn.model_selection import cross_val_score", 21),
    ("Bias-Variance Tradeoff", "bias-variance", "Tradeoff", "overfitting underfitting", "balance bias variance", 22),
    ("Overfitting Underfitting", "overfitting", "Fit issues", "train test split", "from sklearn.model_selection import train_test_split", 23),
    ("Regularization", "regularization", "L1 L2", "Ridge Lasso", "from sklearn.linear_model import Ridge", 24),
    ("LASSO Regression", "lasso", "L1", "Lasso", "from sklearn.linear_model import Lasso", 25),
    ("Ridge Regression", "ridge", "L2", "Ridge", "from sklearn.linear_model import Ridge", 26),
    ("Elastic Net", "elastic-net", "Combined", "ElasticNet", "from sklearn.linear_model import ElasticNet", 27),
    ("Neural Networks Intro", "neural-networks", "NN intro", "MLPClassifier", "from sklearn.neural_network import MLPClassifier", 28),
    ("Perceptrons", "perceptrons", "Neuron", "Perceptron", "from sklearn.linear_model import Perceptron", 29),
    ("Activation Functions", "activation-functions", "Activations", "ReLU sigmoid", "ReLU sigmoid tanh", 30),
    ("Backpropagation", "backpropagation", "Learning", "gradient", "gradient descent backpropagation", 31),
    ("CNN Basics", "cnn-basics", "Image networks", "Conv2D", "from keras.layers import Conv2D", 32),
    ("CNN Architecture", "cnn-architecture", "Networks", "VGG ResNet", "VGG ResNet MobileNet", 33),
    ("Object Detection", "object-detection", "Detection", "YOLO R-CNN", "YOLO R-CNN", 34),
    ("RNN Basics", "rnn-basics", "Sequential", "SimpleRNN", "from keras.layers import SimpleRNN", 35),
    ("LSTM", "lstm", "Memory", "LSTM", "from keras.layers import LSTM", 36),
    ("NLP Basics", "nlp-basics", "Text", "NLP", "text processing", 37),
    ("Text Preprocessing", "text-preprocessing", "Cleaning", "tokenize", "tokenize stem stopwords", 38),
    ("Sentiment Analysis", "sentiment-analysis", "Opinion", "sentiment", "positive negative", 39),
    ("Word Embeddings", "word-embeddings", "Vectors", "Word2Vec", "Word2Vec GloVe", 40),
    ("Transformers", "transformers", "Attention", "BERT GPT", "BERT GPT", 41),
    ("BERT", "bert", "Encoder", "BertModel", "from transformers import BertModel", 42),
    ("GPT Basics", "gpt-basics", "Generator", "GPT2", "from transformers import GPT2LMHeadModel", 43),
    ("Transfer Learning", "transfer-learning", "Fine-tuning", "fine-tune", "fine-tune pretrained", 44),
    ("YOLO", "yolo", "Detection", "YOLO", "YOLO object detection", 45),
    ("Face Recognition", "face-recognition", "Faces", "dlib", "face_recognition library", 46),
    ("Style Transfer", "style-transfer", "Art", "StyleTransfer", "Neural Style Transfer", 47),
    ("GANs", "gans", "Generative", "Generator Discriminator", "Generator Discriminator", 48),
    ("Reinforcement Learning", "rl-learning", "RL", "Q-learning", "Q-learning policy gradient", 49),
    ("RL Algorithms", "rl-algorithms", "Algorithms", "PPO A2C", "PPO A2C DQN", 50),
]

for i, title, slug, starter, solution, num in ml_topics:
    lesson = Lesson(course_id=3, lesson_number=num, title=title, slug=slug,
                  description=f"Learn {title}", content=starter, theory=starter, order=num)
    db.add(lesson)
    db.flush()
    lab = Lab(lesson_id=lesson.id, title=f"Practice {title}", description=f"Practice {title}",
            starter_code=starter, solution=solution, hints="Try it", order=num)
    db.add(lab)


more_topics = [
    ("HTML Basics", "html-basics", "Web structure", "<html></html>", "<html><body>Hi</body></html>", 1),
    ("CSS Fundamentals", "css-fundamentals", "Styling", "p{}", "p { color: blue; }", 2),
    ("CSS Selectors", "css-selectors", "Selection", ".class", ".btn { color: red; }", 3),
    ("CSS Box Model", "css-box-model", "Box model", "margin padding", "div { margin: 10px; padding: 5px; }", 4),
    ("Flexbox Basics", "flexbox", "Layout", "display: flex", "div { display: flex; }", 5),
    ("CSS Grid", "css-grid", "Grid layout", "grid-template", "div { display: grid; }", 6),
    ("Responsive Design", "responsive-design", "Mobile", "@media", "@media (max-width: 768px) {}", 7),
    ("JavaScript Variables", "js-variables", "JS data", "let x", "let name = 'Alice';", 8),
    ("JavaScript Functions", "js-functions", "Functions", "function", "function add(a,b){ return a+b; }", 9),
    ("DOM Manipulation", "dom", "HTML access", "getElementById", "document.getElementById('app')", 10),
    ("Event Listeners", "events", "Interactions", "addEventListener", "element.addEventListener('click', fn)", 11),
    ("Form Validation", "form-validation", "Validation", "checkValidity", "form.checkValidity()", 12),
    ("JSON Basics", "json-basics", "Data format", "JSON.parse", "JSON.parse('{}')", 13),
    ("AJAX Fetch", "ajax-fetch", "Requests", "fetch", "fetch('/api').then(r=>r.json())", 14),
    ("RESTful APIs", "restful-apis", "API design", "GET POST", "GET POST PUT DELETE", 15),
    ("MVC Pattern", "mvc-pattern", "Architecture", "MVC", "Model View Controller", 16),
    ("SQL Basics", "sql-basics", "Database", "SELECT", "SELECT * FROM users", 17),
    ("SELECT Queries", "select-queries", "Read data", "WHERE ORDER", "SELECT * FROM users WHERE id = 1", 18),
    ("INSERT UPDATE", "insert-update", "Write data", "INSERT UPDATE", "INSERT INTO users VALUES(1,'a')", 19),
    ("JOINs", "sql-joins", "Combine", "JOIN", "SELECT * FROM a JOIN b ON a.id=b.a_id", 20),
    ("SQLite Python", "sqlite-python", "SQLite", "sqlite3", "import sqlite3; conn=sqlite3.connect('d')", 21),
    ("SQLAlchemy Basics", "sqlalchemy-basics", "ORM", "Session", "from sqlalchemy import Column", 22),
    ("Git Installation", "git-installation", "Setup", "git config", "git config --global user.name ''", 23),
    ("Git Basics", "git-basics", "VC basics", "add commit", "git add . && git commit -m 'init'", 24),
    ("Git Branches", "git-branches", "Branches", "branch checkout", "git branch feature", 25),
    ("Git Merging", "git-merging", "Merge", "merge", "git merge feature", 26),
    ("GitHub Workflow", "github-workflow", "Remote", "push pull", "git push origin main", 27),
    ("Docker Basics", "docker-basics", "Containers", "docker run", "docker run ubuntu", 28),
    ("Docker Commands", "docker-commands", "CLI", "docker ps", "docker ps build rm", 29),
    ("Docker Compose", "docker-compose", "Multi-container", "docker-compose.yml", "docker-compose up", 30),
    ("CI/CD Basics", "ci-cd", "Automation", "GitHub Actions", "name: CI", 31),
    ("Testing pytest", "pytest-basics", "Tests", "assert", "def test(): assert 1+1==2", 32),
    ("Test Fixtures", "test-fixtures", "Setup", "fixture", "@pytest.fixture", 33),
    ("Mocking", "mocking", "Fakes", "Mock", "from unittest.mock import Mock", 34),
    ("Deployment", "deployment", "Deploy", "Heroku Vercel", "git push heroku main", 35),
    ("Heroku Deployment", "heroku-deployment", "Heroku", "heroku CLI", "heroku create app", 36),
    ("Vercel Netlify", "vercel-netlify", "Static", "Deploy", "Drag drop", 37),
    ("Environment Variables", "env-vars", "Config", "os.environ", "import os; os.environ.get('KEY')", 38),
    ("Configuration", "configuration", "Settings", "config", "config files", 39),
    ("Logging", "logging-practices", "Logging", "logging.info", "logging.basicConfig()", 40),
    ("Security Basics", "security-basics", "Security", "HTTPS XSS", "Sanitize input", 41),
    ("HTTPS SSL", "https-ssl", "Encryption", "TLS SSL", "certbot", 42),
    ("Caching", "caching", "Cache", "Redis", "redis cache", 43),
    ("Redis Basics", "redis-basics", "Cache DB", "SET GET", "redis.Redis()", 44),
    ("Async Python", "async-python", "AsyncIO", "async def", "async def f(): await f()", 45),
    ("asyncio", "asyncio-basics", "Async I/O", "await", "asyncio.run(f())", 46),
    ("WebSockets", "websockets", "Real-time", "WebSocket", "websocket library", 47),
    ("GraphQL Basics", "graphql-basics", "Query lang", "type Query", "type Query { users: [User] }", 48),
    ("Apollo Server", "apollo-server", "GraphQL server", "Apollo", "ApolloServer", 49),
    ("TypeScript Intro", "typescript-intro", "Typed JS", "let x: number", "let x: number = 5;", 50),
]

for i, title, slug, starter, solution, num in more_topics:
    lesson = Lesson(course_id=2, lesson_number=num, title=title, slug=slug,
                  description=f"Learn {title}", content=starter, theory=starter, order=num)
    db.add(lesson)
    db.flush()
    lab = Lab(lesson_id=lesson.id, title=f"Practice {title}", description=f"Practice {title}",
            starter_code=starter, solution=solution, hints="Try it", order=num)
    db.add(lab)

db.commit()
lessons = db.query(Lesson).count()
labs = db.query(Lab).count()
print(f"Total lessons: {lessons}")
print(f"Total labs: {labs}")
db.close()