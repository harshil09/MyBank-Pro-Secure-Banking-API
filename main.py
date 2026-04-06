"""
Banking API with OAuth2 and JWT Authentication

This FastAPI application provides a secure banking system with:
- User registration and authentication (email/password and Google OAuth)
- Account management (balance, deposits, withdrawals)
- Transaction history tracking
- JWT-based session management

Security:
    - Passwords hashed with Argon2
    - JWT tokens for API authentication
    - Google OAuth 2.0 integration

Environment Variables Required:
    - GOOGLE_CLIENT_ID: Google OAuth client ID
    - GOOGLE_CLIENT_SECRET: Google OAuth client secret
    - GOOGLE_REDIRECT_URI: OAuth callback URL (default: http://localhost:5000/auth/google/callback)
"""
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from database import get_connection
from models import create_table
from schemas import User,Transactions
from jose import jwt
from datetime import datetime,timedelta
from passlib.context import CryptContext
from authlib.integrations.starlette_client import OAuth
import os #Access system & environment variables
from dotenv import load_dotenv #Import function to read .env file

#Load .env into environment
load_dotenv()

# Password hashing context using Argon2 (OWASP recommended)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Hash password
def hash_password(password: str) -> str:
    """
    Hash a plain text password using Argon2.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        str: Argon2 hashed password string
        
    Note:
        Uses passlib's Argon2 scheme with automatic salt generation
    """
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Argon2 hash to check against
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

# Security Configuration
SECRET_KEY = "MYSECRETKEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60

#CREATE TOKEN
def create_access_token(data:dict):
    """
    Generate a JWT access token.
    
    Creates a signed JWT token with expiration time.
    
    Args:
        data: Payload data to encode in token (typically user_id, email)
        
    Returns:
        str: Encoded JWT token
        
    Note:
        Token expires in ACCESS_TOKEN_EXPIRE_MINUTES (60 minutes)
        Signed with HS256 algorithm using SECRET_KEY
    """
    to_encode=data.copy()
    expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)

#VERIFY TOKEN
def verify_token(authorization:str):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token missing")
    try:
        token = authorization.split(" ")[1]   # Bearer <token>
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

app = FastAPI(
    title="Banking API",
    description="""
    A secure banking API with OAuth2 and JWT authentication.
    
    ## Features
    * User registration with email/password
    * Google OAuth 2.0 integration
    * Secure password hashing (Argon2)
    * JWT token-based authentication
    * Account balance management
    * Deposit and withdrawal operations
    * Transaction history tracking
    
    ## Authentication
    Most endpoints require a JWT token in the Authorization header:
    Authorization: Bearer <your_jwt_token>
    """

)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

#instance 
oauth=OAuth()

#register google as provider
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={'scope': 'openid email profile'},

)

create_table()

#STEP1: REDIRECT TO GOOGLE
@app.get("/auth/google/login")
async def google_login(request:Request):
    #if not os.getenv("GOOGLE_CLIENT_ID") or not os.getenv("GOOGLE_CLIENT_SECRET"):
     #   raise HTTPException(
      #      status_code=500,
       #     detail="Google OAuth is not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env",
       # )
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:5000/auth/google/callback")
    # prompt=select_account forces Google's account UI instead of silently reusing the browser session
    return await oauth.google.authorize_redirect(
        request, redirect_uri, prompt="select_account"
    )

#STEP 2: Google redirects back
@app.get("/auth/google/callback")
async def google_callback(request: Request):
    #STEP 3: Exchange code for token
    token = await oauth.google.authorize_access_token(request)
    #STEP 4: Get user info
    user_info = token.get("userinfo")
    #Fallback (very important)
    if not user_info:#if token didnt contain user info
        #call google api to get a response object like(requests.response)
        user_info = await oauth.google.get("userinfo", token=token)
        #convert response into json format
        user_info = user_info.json()
    email = user_info.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Google account missing email")
    display_name = user_info.get("name") or " ".join(
        p for p in (user_info.get("given_name"), user_info.get("family_name")) if p
    ).strip()
    if not display_name:
        display_name = email.split("@")[0]
    conn=get_connection()
    cursor=conn.cursor()
    # Check if user exists
    cursor.execute("SELECT id FROM users WHERE email=?", (email,))
    result = cursor.fetchone()

    if not result:
        #create new user
        # Password is nullable in schema, so Google users can be created without password.
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, None))
        user_id=cursor.lastrowid
        cursor.execute("INSERT INTO accounts (user_id,balance) VALUES (?,0)", (user_id,))
        conn.commit()
    else:
        user_id=result[0]
    conn.close()

    # Issue JWT (Google "name" is used for dashboard welcome, e.g. "Harshil Soni")
    jwt_token = create_access_token(
        {"user_id": user_id, "email": email, "name": display_name}
    )
    #return RedirectResponse(url=f"http://127.0.0.1:8501/?token={jwt_token}", status_code=302)

    return RedirectResponse(
    url=f"https://your-streamlit-app.streamlit.app/?token={jwt_token}",
    status_code=302)


@app.post("/signup")
def SignUp(user: User):
    """
    Register a new user with email and password.
    
    Creates a new user account with hashed password (Argon2) and initializes
    an associated account with zero balance.
    
    Args:
        user: User credentials (email and password)
    
    Returns:
        dict: Success message upon account creation
        
    Raises:
        HTTPException: 400 if email already exists in the database
        
    Example:
```json
        {
            "email": "user@example.com",
            "password": "securePassword123"
        }
```
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email=?", (user.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email already exists")
          # Hash password
        hashed_password = hash_password(user.password)  # 🔑 hash password
         # Insert new user
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)",
                       (user.email, hashed_password))
        user_id = cursor.lastrowid
         # Create account with 0 balance
        cursor.execute("INSERT INTO accounts (user_id, balance) VALUES (?, ?)", (user_id, 0))
        conn.commit()
        return {"message": "User created successfully"}

    finally:
        conn.close()
    #cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (user.email, user.password))
    #user_id = cursor.lastrowid
    #conn.commit()
    #conn.close()
    #return {"message": "User created"}

@app.post("/login")
def Login(user: User):
    """
    Authenticate user and return JWT access token.
    
    Verifies user credentials against hashed password in database.
    Creates account record if missing. Returns JWT token valid for 60 minutes.
    
    Args:
        user: User credentials (email and password)
    
    Returns:
        dict: Contains success message and JWT access_token
        
    Raises:
        HTTPException: 401 if credentials are invalid
        
    Security:
        Token expires in 60 minutes (ACCESS_TOKEN_EXPIRE_MINUTES)
    """
    conn = get_connection()
    cursor = conn.cursor()
    # fetch user by email
    cursor.execute(
        "SELECT id,password FROM users WHERE email=?",
        (user.email,),
    )
    result = cursor.fetchone()

    if not result or not verify_password(user.password, result[1]): # 🔑 verify hashed password
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user_id = result[0]
    # ensure account exists
    cursor.execute("SELECT 1 FROM accounts WHERE user_id=?", (user_id,))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO accounts (user_id, balance) VALUES (?, 0)", (user_id,)
        )
    conn.commit()
    conn.close()
    token = create_access_token({"user_id": user_id})

    return {
    "message": "Login successful",
    "access_token": token
    }
    #return {"message": "Login successful", "user_id": user_id}

#GET BALANCE
@app.get("/balance")
def get_balance(authorization: str = Header(None)):
    """
    Retrieve the current balance for the authenticated user.
    
    Requires valid JWT token in Authorization header.
    
    Args:
        authorization: Bearer token in format "Bearer <token>"
    
    Returns:
        dict: Current account balance
        
    Raises:
        HTTPException: 401 if token is invalid or missing
        HTTPException: 404 if user account not found
        
    Example Response:
```json
        {
            "balance": 1500.50
        }
```
    """

    print("Authorization header:", authorization)
    payload=verify_token(authorization)
    user_id=payload["user_id"]
    print("Authorization:", authorization)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT balance FROM accounts WHERE user_id=?", (user_id,)
    )
    result = cursor.fetchone()
    conn.close()

    if result is not None:
        return {"balance": result[0]}
    raise HTTPException(status_code=404, detail="user not found")

#Deposit
@app.post("/deposit")
def Deposit(txt: Transactions, authorization: str = Header(None)):
    """Deposit funds into authenticated user's account."""
    payload = verify_token(authorization)
    user_id = payload["user_id"]
    conn = get_connection()
    cursor=conn.cursor()
    # Update account balance atomically
    cursor.execute("UPDATE accounts SET balance = balance + ? WHERE  user_id=?", (txt.amount, user_id))
    # Record transaction for audit trail
    cursor.execute("INSERT INTO transactions (user_id,type,amount) VALUES (?, 'deposit', ?)", (user_id,txt.amount))
    conn.commit()
    # Fetch updated balance for confirmation
    cursor.execute("SELECT balance FROM accounts WHERE user_id=?", (user_id,))
    balance = cursor.fetchone()[0]
    conn.close()
    return {"message": "Deposit successful", "balance": balance}

#Withdraw
@app.post("/withdraw")
def withdraw(txt:Transactions, authorization: str = Header(None)):
    #token = authorization.split(" ")[1]
    payload = verify_token(authorization)
    user_id = payload["user_id"]
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT balance FROM accounts where user_id=? ", (user_id,))
    balance=cursor.fetchone()[0]
    if txt.amount>balance:
        conn.close()
        raise HTTPException(status_code=400, detail="Insufficient funds")
    cursor.execute("UPDATE accounts SET balance= balance - ? WHERE user_id=?", (txt.amount, user_id))
    cursor.execute("INSERT INTO transactions (user_id,type,amount) VALUES (?, 'withdraw', ?)", (user_id,txt.amount))
    conn.commit()
    cursor.execute('SELECT balance FROM accounts WHERE user_id=?', (user_id,))
    new_balance=cursor.fetchone()[0]
    conn.close()
    return {"message": "Withdrawal successful", "balance": new_balance}


@app.get("/transactions")
def get_transactions(authorization: str = Header(None)):

    #if authorization is None:
     #   raise HTTPException(status_code=401, detail="Token missing")

    #token = authorization.split(" ")[1]
    payload = verify_token(authorization)
    user_id = payload["user_id"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT amount, type, timestamp FROM transactions WHERE user_id=?", (user_id,))

    rows = cursor.fetchall()
    conn.close()

    # Convert to JSON
    transactions = []
    for row in rows:
        transactions.append({
            "amount": row[0],
            "type": row[1],
            "timestamp": row[2]
        })

    return transactions




