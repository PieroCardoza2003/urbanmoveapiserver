from fastapi import APIRouter, Depends, File, UploadFile
from typing import Optional
from sqlalchemy.orm import Session
from middlewares.auth import verify_access_token
from fastapi import HTTPException
from database.db import get_db
from schemas.ConductorScheme import ConductorEmpresaCreate, ConductorPrivadoCreate
from controller.ConductorController import conductor_empresa_create, conductor_privado_create


router = APIRouter(prefix="/driver")

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/*"}

@router.post("/register-private")
async def create_conductor_privado(
    conductor: ConductorPrivadoCreate = Depends(),
    fotoperfil: Optional[UploadFile] = File(None),
    licencia_frontal: UploadFile = File(...),
    licencia_reverso: UploadFile = File(...),
    db: Session = Depends(get_db)):

    if fotoperfil and fotoperfil.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="fotoperfil debe ser una imagen.")

    if licencia_frontal.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="licencia_frontal debe ser una imagen.")

    if licencia_reverso.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="licencia_reverso debe ser una imagen.")
    
    return await conductor_privado_create(
        conductor=conductor, 
        fotoperfil=fotoperfil,
        licenciafrontal=licencia_frontal,
        licenciareverso=licencia_reverso,
        db=db)



@router.post("/register-company")
async def create_conductor_empresa(
    conductor: ConductorEmpresaCreate = Depends(),
    fotoperfil: Optional[UploadFile] = File(None),
    licencia_frontal: UploadFile = File(...),
    licencia_reverso: UploadFile = File(...),
    db: Session = Depends(get_db)):

    if fotoperfil and fotoperfil.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="fotoperfil debe ser una imagen.")

    if licencia_frontal.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="licencia_frontal debe ser una imagen.")

    if licencia_reverso.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="licencia_reverso debe ser una imagen.")
    
    return await conductor_empresa_create(
        conductor=conductor, 
        fotoperfil=fotoperfil,
        licenciafrontal=licencia_frontal,
        licenciareverso=licencia_reverso,
        db=db)