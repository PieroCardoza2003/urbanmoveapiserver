from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from middlewares.auth import verify_access_token
from fastapi import HTTPException
from database.db import get_db
from schemas.UsuarioScheme import UsuarioCreate, UsuarioLogin, GoogleLogin, UsuarioFind, UsuarioCode, UsuarioPassword, UsuarioToken
from controller.UsuarioController import user_get_all, user_get_one, user_create, user_login, google_login, account_verify, code_verify, password_new, session_verify, accesstoken_renew, driver_get_one


router = APIRouter(prefix="/user")


@router.get("/list/all")
def get_all_users(db: Session = Depends(get_db)):
    return user_get_all(db=db)


#@router.get("/get/{id}", dependencies=[Depends(verify_access_token)])
#def get_one_user(id, db: Session = Depends(get_db)):
#    return user_get_one(db=db, id=id)

@router.get("/get-user")
def get_one_user(db: Session = Depends(get_db), payload: dict = Depends(verify_access_token)):
    id = payload.get("sub")
    if not id:
        raise HTTPException(status_code=400, detail="Token error")
    return user_get_one(db=db, id=id)


@router.get("/verify-driver")
def get_one_driver(db: Session = Depends(get_db), payload: dict = Depends(verify_access_token)):
    id = payload.get("sub")
    if not id:
        raise HTTPException(status_code=400, detail="Token error")
    return driver_get_one(db=db, id=id)



@router.get("/verify-session")
def verify_session(db: Session = Depends(get_db), payload: dict = Depends(verify_access_token)):
    id = payload.get("sub")
    if not id:
        raise HTTPException(status_code=400, detail="Token error")
    return session_verify(db=db, id=id)


@router.post("/access-token")
def renew_accesstoken(token: UsuarioToken, db: Session = Depends(get_db)):
    return accesstoken_renew(db=db, token=token)


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
def login_user(user: UsuarioLogin, db: Session = Depends(get_db), request: Request = None):
    
    client_ip = request.headers.get("X-Forwarded-For")

    if client_ip:
        client_ip = client_ip.split(",")[0].strip()
    else:
        client_ip = request.client.host
    
    return user_login(db=db, user=user, client_ip=client_ip)


@router.post("/login-google")
def login_google(user: GoogleLogin, db: Session = Depends(get_db), request: Request = None):

    client_ip = request.headers.get("X-Forwarded-For")

    if client_ip:
        client_ip = client_ip.split(",")[0].strip()
    else:
        client_ip = request.client.host

    return google_login(db=db, user=user, client_ip=client_ip)
