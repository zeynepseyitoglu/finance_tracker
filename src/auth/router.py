from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.async_database import get_db
from src.auth.schemas import UserCreate, UserResponse, LoginRequest
from src.auth.crud import get_user_by_email, create_user
from src.auth.hashing import verify_password
from src.auth.jwt import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.dependencies import get_current_user
from src.db_models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Register User", description="Registers a new user with email and password. Returns the created user")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_email(db, user.email) #returns None if user doesn't exist
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    new_user = await create_user(db, user)
    return new_user

@router.post("/login", summary="Login User", description="Logs in a user with email and password. Returns 200 if successful, 401 if credentials are invalid")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    access_token = create_access_token(data={"email": user.email})
    return {'access_token': access_token,'token_type': 'bearer'}

@router.get("/me", response_model=UserResponse, summary='Get current user', description='Returns the currently logged in user')
async def get_current_user_details(current_user: User = Depends(get_current_user)):
    return current_user