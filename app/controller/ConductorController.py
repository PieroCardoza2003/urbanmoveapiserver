from fastapi import File, UploadFile
from typing import Optional
from pathlib import Path

from models.Conductor import Conductor
from models.Usuario import Usuario
from models.Empleado import Empleado

from models.ConductorEmpresa import ConductorEmpresa
from models.ConductorPrivado import ConductorPrivado

from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from utils.string_utils import is_blank
from utils.email_utils import verify_email
from utils.bcrypt_utils import encode_password, verify_password
from utils.randomcode_utils import generar_codigo_unico
from utils.image_base64_utils import image_to_base64
from services.github_repo_service import upload_image
from schemas.ConductorScheme import ConductorEmpresaCreate

async def conductor_empresa_create(
    conductor: ConductorEmpresaCreate,
    fotoperfil: Optional[UploadFile],
    licencia_frontal: UploadFile,
    licencia_reverso: UploadFile,
    db: Session):
        
    usuario = db.query(Usuario).filter_by(id_usuario=conductor.id_usuario).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="User not found")
    
    isConductor = db.query(Conductor).filter_by(id_usuario=conductor.id_usuario).first()

    if isConductor:
        raise HTTPException(status_code=400, detail="Driver already exist")
    
    isConductorEmpresa = db.query(ConductorEmpresa).filter_by(codigo_empleado=conductor.codigo_empleado).first()
    
    if isConductorEmpresa:
        raise HTTPException(status_code=400, detail="Employee code already exist")
    
    #isEmpleado = db.query(Empleado).filter_by(codigo_empleado=conductor.codigo_empleado,).first()
    
    


    # Extraer las extensiones de las imagenes

    if fotoperfil:
        fotoperfil_extension = Path(fotoperfil.filename).suffix.lower()
    else:
        fotoperfil_extension = None
    
    licencia_frontal_extension = Path(licencia_frontal.filename).suffix.lower()
    licencia_reverso_extension = Path(licencia_reverso.filename).suffix.lower()

    # convertir las imagenes a bytes

    fotoperfil = await fotoperfil.read() if fotoperfil else conductor.foto_perfil
    licencia_frontal = await licencia_frontal.read() if licencia_frontal else None
    licencia_reverso = await licencia_reverso.read() if licencia_reverso else None

    if not fotoperfil or not licencia_frontal or not licencia_reverso:
        raise HTTPException(status_code=400, detail="No data provided")
    

    
    try:
        # Subir y obtener url foto perfil del repositorio de github
        if not isinstance(fotoperfil, str):
            fotoperfil = await upload_image(image_bytes=fotoperfil, extension=fotoperfil_extension)

        # Subir y obtener url licencia frontal
        if licencia_frontal:
            licencia_frontal = await upload_image(image_bytes=licencia_frontal, extension=licencia_frontal_extension)

        # Subir y obtener url licencia reverso
        if licencia_reverso:
            licencia_reverso = await upload_image(image_bytes=licencia_reverso, extension=licencia_reverso_extension)

        if not fotoperfil or not licencia_frontal or not licencia_reverso:
            raise HTTPException(status_code=400, detail="No data provided")  
        



        return None
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")

