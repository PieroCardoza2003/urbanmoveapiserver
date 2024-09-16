from models.Usuario import Usuario
from sqlalchemy.orm import Session
from fastapi import HTTPException
from utils.uuid_utils import verify_uuid
from utils.email_utils import verify_email
from utils.bcrypt_utils import encode_password
from schemas.UsuarioScheme import UsuarioCreate


def user_get_all(db: Session):
    return db.query(Usuario).all()


def user_get_one(db: Session, id: str):
    
    if not verify_uuid(id):
        raise HTTPException(status_code=400, detail="Bad request")

    usuario = db.query(Usuario).filter_by(id_usuario=id).first()

    if usuario is None:
        raise HTTPException(status_code=404, detail="User not found")

    return usuario


def user_create(db: Session, user: UsuarioCreate):

        if not verify_email(user.email_usuario):
            raise HTTPException(status_code=400, detail="Invalid email")
        

        existing_user = db.query(Usuario).filter_by(email_usuario=user.email_usuario).first()

        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        

        db_user = Usuario(
                nombres_usuario=user.nombres_usuario,
                apellidos_usuario=user.apellidos_usuario,
                fecha_nacimiento_usuario=user.fecha_nacimiento_usuario,
                email_usuario=user.email_usuario,
                password_usuario=encode_password(user.password_usuario)
            )

        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")


    
    