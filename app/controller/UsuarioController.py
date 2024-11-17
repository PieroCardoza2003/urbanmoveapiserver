from models.Usuario import Usuario

from models.Conductor import Conductor
from models.ConductorEmpresa import ConductorEmpresa
from models.ConductorPrivado import ConductorPrivado

from models.UsuarioSesion import UsuarioSesion
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from utils.uuid_utils import verify_uuid, get_uuid
from utils.datetime_utils import datetime_now
from utils.email_utils import verify_email
from utils.bcrypt_utils import encode_password, verify_password
from utils.string_utils import is_blank
from utils.jwt_utils import get_access_token, get_refresh_token
from services.google_auth_service import verify_token
from services.smtp_service import send_verifycode
from utils.jwt_utils import verify_refresh_token
from services.activate_user_service import generate_random_code, prints_users, validate_code
from schemas.UsuarioScheme import UsuarioCreate, UsuarioLogin, GoogleLogin, UsuarioId, UsuarioFind, UsuarioCode, UsuarioPassword, UsuarioToken, UsuarioResponse, UsuarioConductorResponse


def user_get_all(db: Session):
    return db.query(Usuario).all()


def accesstoken_renew(db: Session, token: UsuarioToken):
    payload = verify_refresh_token(token=token.token)

    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    id = payload.get("sub")
    
    usuario = db.query(Usuario).filter_by(id_usuario=id).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing_sesion = db.query(UsuarioSesion).filter_by(id_usuario=usuario.id_usuario, token=token.token).first()

    if not existing_sesion:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    access_token_user = get_access_token(id=id)

    return JSONResponse(content={ 
            "token": access_token_user[1]
        }, status_code=200)


def session_verify(db: Session, id: str):
    usuario = db.query(Usuario).filter_by(id_usuario=id).first()

    if usuario is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return JSONResponse(content={ 
            "id_usuario": f"{usuario.id_usuario}",
            "rol_actual": usuario.rol_actual
        }, status_code=200)



def user_get_one(db: Session, id: str):
    
    if not verify_uuid(id):
        raise HTTPException(status_code=400, detail="Bad request")

    usuario = db.query(Usuario).filter_by(id_usuario=id).first()

    if usuario is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        # cambiar a modo pasajero
        usuario.rol_actual = "PASAJERO"
        db.commit()  

        return UsuarioResponse(
            id_usuario=usuario.id_usuario,
            nombres=usuario.nombres,
            apellidos=usuario.apellidos,
            foto_perfil=usuario.foto_perfil
        )
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")


def driver_get_one(db: Session, id: str):

    usuario = db.query(Usuario).filter_by(id_usuario=id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="User not found")
    
    conductor = db.query(Conductor).filter_by(id_usuario=usuario.id_usuario).first()
    
    id_conductor = None
    tipo_conductor = None

    if conductor:
        if conductor.tipo_conductor == "EMPRESA":
            isConductor = db.query(ConductorEmpresa).filter_by(id_conductor=conductor.id_conductor).first()
            if isConductor:
                id_conductor = isConductor.id_conductor
                tipo_conductor = "EMPRESA"
        
        elif conductor.tipo_conductor == "PRIVADO":
            isConductor = db.query(ConductorPrivado).filter_by(id_conductor=conductor.id_conductor).first()
            if isConductor:
                id_conductor = isConductor.id_conductor
                tipo_conductor = "PRIVADO"
  
    try:
        # cambiar a modo conductor
        usuario.rol_actual = "CONDUCTOR"
        db.commit()  
        
        return UsuarioConductorResponse(
            id_usuario=usuario.id_usuario,
            nombres=usuario.nombres,
            apellidos=usuario.apellidos,
            fecha_nacimiento=usuario.fecha_nacimiento,
            foto_perfil=usuario.foto_perfil,
            id_conductor=id_conductor,
            tipo_conductor=tipo_conductor
        )
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")


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



def google_login(db: Session, user: GoogleLogin, client_ip: str):

    token = user.token

    if is_blank(token):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    data = verify_token(token) # (nombre, email)

    if not data:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    existing_user = db.query(Usuario).filter_by(email=data[1]).first()

    if existing_user and existing_user.tipo_autenticacion != "GOOGLE":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not existing_user:
        
        user = UsuarioCreate(
            nombres=data[0],
            apellidos=None,
            fecha_nacimiento=None,
            email=data[1],
            password=None
        )

        result = insert_user(db=db, user=user, authtype="GOOGLE")
        
        if result == 1:
            raise HTTPException(status_code=500, detail="Internal server error")
        
        existing_user = UsuarioId(id_usuario=result)

    # VERIFICAR SI EXISTE UNA SESSION Y REEMPLAZARLA
    existing_sesion = db.query(UsuarioSesion).filter_by(id_usuario=existing_user.id_usuario).first()

    access_token_user = get_access_token(existing_user.id_usuario)
    refresh_token_user = get_refresh_token(existing_user.id_usuario)

    if not existing_sesion:
        new_session = UsuarioSesion(
            id_usuario = existing_user.id_usuario,
            ip_usuario = client_ip,
            token = refresh_token_user[1],
            fecha_creacion = refresh_token_user[0].get("iat"),
            fecha_expiracion = refresh_token_user[0].get("exp")
        )

        db.add(new_session)
        db.commit()
        db.refresh(new_session)

    else:
        existing_sesion.id_sesion = get_uuid()
        existing_sesion.ip_usuario = client_ip
        existing_sesion.token = refresh_token_user[1]
        existing_sesion.fecha_creacion = refresh_token_user[0].get("iat")
        existing_sesion.fecha_expiracion = refresh_token_user[0].get("exp")
        db.commit()


    return JSONResponse(content={
            "access_token": access_token_user[1],
            "refresh_token": refresh_token_user[1],
            "role": existing_user.rol_actual
        }, status_code=200)


def user_login(db: Session, user: UsuarioLogin, client_ip: str):

    user_email = user.email.strip()
    user_password = user.password.strip()

    if not verify_email(user_email) or is_blank(user_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    existing_user = db.query(Usuario).filter_by(email=user_email, tipo_autenticacion="LOCAL").first()
    
    if not existing_user or not verify_password(existing_user.password, user_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # VERIFICAR SI EXISTE UNA SESSION Y REEMPLAZARLA
    existing_sesion = db.query(UsuarioSesion).filter_by(id_usuario=existing_user.id_usuario).first()

    access_token_user = get_access_token(existing_user.id_usuario)
    refresh_token_user = get_refresh_token(existing_user.id_usuario)

    if not existing_sesion:
        new_session = UsuarioSesion(
            id_usuario = existing_user.id_usuario,
            ip_usuario = client_ip,
            token = refresh_token_user[1],
            fecha_creacion = refresh_token_user[0].get("iat"),
            fecha_expiracion = refresh_token_user[0].get("exp")
        )

        db.add(new_session)
        db.commit()
        db.refresh(new_session)

    else:
        existing_sesion.id_sesion = get_uuid()
        existing_sesion.ip_usuario = client_ip
        existing_sesion.token = refresh_token_user[1]
        existing_sesion.fecha_creacion = refresh_token_user[0].get("iat")
        existing_sesion.fecha_expiracion = refresh_token_user[0].get("exp")
        db.commit()
    
    return JSONResponse(content={
            "access_token": access_token_user[1],
            "refresh_token": refresh_token_user[1],
            "role": existing_user.rol_actual
        }, status_code=200)


def insert_user(db: Session, user: UsuarioCreate, authtype: str):
    try:
        usuarioId = get_uuid()

        result = db.execute(text("""
            SELECT registra_usuario_pasajero(
                :id_usuario,
                :nombres,
                :apellidos,
                :fecha_nacimiento,
                :email,
                :password,
                :foto_perfil,
                :ciudad,
                :rol_actual,
                :tipo_autenticacion,
                :fecha_registro,
                :id_pasajero
            )
        """), {
                "id_usuario": usuarioId,
                "nombres": user.nombres,
                "apellidos": user.apellidos,
                "fecha_nacimiento": user.fecha_nacimiento,
                "email": user.email,
                "password":  encode_password(user.password) if user.password else None,
                "foto_perfil": None,
                "ciudad": None,
                "rol_actual": "PASAJERO",
                "tipo_autenticacion": authtype,
                "fecha_registro": str(datetime_now()),
                "id_pasajero": get_uuid()
            }
        ).scalar() 

        db.commit()

        if result != 0:
            return 1
        
        return usuarioId 
    except Exception as e:
        print(e)
        return 1


def user_create(db: Session, user: UsuarioCreate):
    
    if not verify_email(user.email):
        raise HTTPException(status_code=400, detail="Invalid email")
    
    existing_user = db.query(Usuario).filter_by(email=user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    try:
        result = insert_user(db=db, user=user, authtype="LOCAL")
        
        if result == 1:
            raise HTTPException(status_code=500, detail="Internal server error")

        return JSONResponse(content= {
                "details": "success"
            }, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


    
    