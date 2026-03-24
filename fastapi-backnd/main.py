from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt  # This is the PyJWT library
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

# --- CONFIGURATION ---
SECRET_KEY = "your-super-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Initialize Argon2 Hasher
ph = PasswordHasher()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

# --- MOCK DATABASE ---
# Pre-hashing the password with Argon2 for the mock DB
MOCK_HASHED_PASSWORD = ph.hash("123456789")

fake_users_db = {
    "rajat": {
        "username": "rajat",
        "email": "rajat@gmail.com",
        "hashed_password": MOCK_HASHED_PASSWORD,
    }
}

# --- SCHEMAS ---
class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    email: str | None = None

# --- UTILS ---
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # PyJWT's encode returns a string directly
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # PyJWT decode logic
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception
    return User(**user)

# --- ROUTES ---

@app.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    try:
        # Argon2 verification
        ph.verify(user_dict["hashed_password"], form_data.password)
        
        # Check if the hash needs re-hashing (if you changed Argon2 parameters later)
        if ph.check_needs_rehash(user_dict["hashed_password"]):
            # In a real app, you'd update the DB here with ph.hash(form_data.password)
            pass
            
    except VerifyMismatchError:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": user_dict["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user