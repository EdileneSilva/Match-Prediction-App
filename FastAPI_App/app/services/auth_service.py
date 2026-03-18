from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.user import User
from ..schemas.user import UserRegister, UserLogin
from ..core.security import get_password_hash, verify_password, create_access_token

class AuthService:
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def register_user(db: Session, user_data: UserRegister):
        # Check if email exists
        if AuthService.get_user_by_email(db, user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cet email est déjà utilisé."
            )
        
        # Check if username exists
        if AuthService.get_user_by_username(db, user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ce nom d'utilisateur est déjà pris."
            )

        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def authenticate_user(db: Session, login_data: UserLogin):
        user = AuthService.get_user_by_email(db, login_data.email)
        if not user:
            return False
        if not verify_password(login_data.password, user.hashed_password):
            return False
        return user

    @staticmethod
    def create_user_token(user: User):
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id}
        )
        return {"access_token": access_token, "token_type": "bearer"}
