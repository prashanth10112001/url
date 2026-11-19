from fastapi import APIRouter, Depends, HTTPException,status

from app.schemas.auth_schema import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.services.auth_service import AuthService, get_auth_service
from app.exceptions.auth_exceptions import EmailAlreadyExists, InvalidCredentials, UsernameAlreadyExists
from app.models.user_model import User
from app.dependencies.auth import get_current_user

auth_controller = APIRouter(
    prefix="/auth",
    tags=["AUTH"]
)

@auth_controller.get("/me", response_model=UserResponse)
def get_me(current_user : User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email
    )


@auth_controller.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    request:RegisterRequest,
    service : AuthService = Depends(get_auth_service)
):
    try:
        user = service.register_user(
            username=request.username,
            email=request.email,
            password=request.password,
        )

        return {
            "message" : "User registered successfully",
            "user_id": user.id
        }
    except UsernameAlreadyExists:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    except EmailAlreadyExists:
    
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )


@auth_controller.post("/login", response_model=TokenResponse)
def login(
    request:LoginRequest,
    service : AuthService = Depends(get_auth_service)
):
    try:
        token = service.login_user(request.username,request.password)

        return TokenResponse(
            access_token=token
        )
    except InvalidCredentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )