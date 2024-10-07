from models.Usuario import Usuario
from models.UsuarioSesion import UsuarioSesion
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from utils.uuid_utils import verify_uuid
from utils.email_utils import verify_email
from utils.bcrypt_utils import encode_password, verify_password
from utils.string_utils import is_blank
from utils.jwt_utils import get_access_token, get_refresh_token
from services.google_auth_service import verify_token
from services.smtp_service import send_verifycode
from services.activate_user_service import generate_random_code, prints_users, validate_code
from schemas.UsuarioScheme import UsuarioCreate, UsuarioLogin, GoogleLogin, UsuarioId, UsuarioFind, UsuarioCode, UsuarioPassword


def user_get_all(db: Session):
    return db.query(Usuario).all()


def user_get_one(db: Session, id: str):
    
    if not verify_uuid(id):
        raise HTTPException(status_code=400, detail="Bad request")

    usuario = db.query(Usuario).filter_by(id_usuario=id).first()

    if usuario is None:
        raise HTTPException(status_code=404, detail="User not found")
    return usuario


def password_new(db: Session, user: UsuarioPassword):
    user_email = user.email.strip()
    user_password = user.password.strip()

    if not verify_email(user_email) or is_blank(user_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    existing_user = db.query(Usuario).filter_by(email=user_email, tipo_autenticacion="LOCAL").first()
    
    if not existing_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    try:
        existing_user.password = encode_password(user.password)
        db.commit()
        return JSONResponse(content={ "details": "OK" }, status_code=200)
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")


def account_verify(db: Session, user: UsuarioFind):
    user_email = user.email.strip()
    type = user.type.strip()

    if not verify_email(user_email) or (type != "FIND_REGISTER" and type != "FIND_RECOVERY"):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    existing_user = db.query(Usuario).filter_by(email=user_email).first()
    
    if existing_user and type == "FIND_REGISTER":
        raise HTTPException(status_code=400, detail="User already exists")
    
    if not existing_user and type == "FIND_RECOVERY":
        raise HTTPException(status_code=404, detail="User not found")
    
    code = generate_random_code()
    send_verifycode(asunto="URBAN MOVE: Código de verificación", email=user_email, code=code)
    
    return JSONResponse(content={ "details": "OK" }, status_code=200)


def code_verify(user: UsuarioCode):
    prints_users()
    
    if not validate_code(email=user.email, code=user.code):
        raise HTTPException(status_code=404, detail="Incorrect code")
    
    return JSONResponse(content={ "details": "OK" }, status_code=200)


def google_login(db: Session, user: GoogleLogin):

    token = user.token

    if is_blank(token):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    data = verify_token(token) # (nombre, email)

    if not data:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    existing_user = db.query(Usuario).filter_by(email=data[1], tipo_autenticacion="GOOGLE").first()

    if not existing_user:

        db_user = Usuario(
            nombres=data[0],
            apellidos=None,
            fecha_nacimiento=None,
            email=data[1],
            password=None,
            foto_perfil=None,
            ciudad=None,
            rol_actual="PASAJERO",
            tipo_autenticacion="GOOGLE"
        )

        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            existing_user = UsuarioId(id_usuario=db_user.id_usuario)
        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error")

    return JSONResponse(content={
        "access_token": get_access_token(existing_user.id_usuario),
        "refresh_token": get_refresh_token(existing_user.id_usuario)
    }, status_code=200)


    


def user_login(db: Session, user: UsuarioLogin):

    user_email = user.email.strip()
    user_password = user.password.strip()
    

    if not verify_email(user_email) or is_blank(user_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    existing_user = db.query(Usuario).filter_by(email=user_email, tipo_autenticacion="LOCAL").first()
    
    if not existing_user or not verify_password(existing_user.password, user_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # VERIFICAR SI EXISTE UNA SESSION Y REEMPLAZARLA
    #existing_sesion = db.query(UsuarioSesion).filter_by(id_usuario=existing_user.id_usuario).first()

    #if existing_sesion:


    
    return JSONResponse(content={
            "access_token": get_access_token(existing_user.id_usuario),
            "refresh_token": get_refresh_token(existing_user.id_usuario)
        }, status_code=200)




def user_create(db: Session, user: UsuarioCreate):

        if not verify_email(user.email):
            raise HTTPException(status_code=400, detail="Invalid email")
        

        existing_user = db.query(Usuario).filter_by(email=user.email).first()

        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        

        db_user = Usuario(
                nombres=user.nombres,
                apellidos=user.apellidos,
                fecha_nacimiento=user.fecha_nacimiento,
                email=user.email,
                password=encode_password(user.password),
                foto_perfil=None,
                ciudad=None,
                rol_actual="PASAJERO",
                tipo_autenticacion="LOCAL"
            )

        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return JSONResponse(content={
                    "details": "success"
                }, status_code=200)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")


    
    