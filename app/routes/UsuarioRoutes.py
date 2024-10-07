from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from database.db import get_db
from schemas.UsuarioScheme import UsuarioCreate, UsuarioLogin, GoogleLogin, UsuarioFind, UsuarioCode, UsuarioPassword
from controller.UsuarioController import user_get_all, user_get_one, user_create, user_login, google_login, account_verify, code_verify, password_new


router = APIRouter(prefix="/user")


@router.get("/list/all")
def get_all_users(db: Session = Depends(get_db)):
    return user_get_all(db=db)


@router.get("/get/{id}")
def get_one_user(id, db: Session = Depends(get_db)):
    return user_get_one(db=db, id=id)


@router.post("/register")
def create_user(user: UsuarioCreate, db: Session = Depends(get_db)):
    return user_create(db=db, user=user)


@router.post("/verify-account")
def verify_account(user: UsuarioFind, db: Session = Depends(get_db)):
    return account_verify(db=db, user=user)


@router.post("/verify-code")
def verify_code(user: UsuarioCode):
    return code_verify(user=user)


@router.post("/new-password")
def new_password(user: UsuarioPassword, db: Session = Depends(get_db)):
    return password_new(db=db, user=user)


@router.post("/login")
def login_user(user: UsuarioLogin, db: Session = Depends(get_db)):
    return user_login(db=db, user=user)


@router.post("/login-google")
def login_google(user: GoogleLogin, db: Session = Depends(get_db)):
    return google_login(db=db, user=user)
