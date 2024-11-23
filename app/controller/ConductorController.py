from fastapi import UploadFile
from typing import Optional
from pathlib import Path
from sqlalchemy import text

from models.Conductor import Conductor
from models.Usuario import Usuario
from models.Empleado import Empleado

from models.ConductorEmpresa import ConductorEmpresa
from models.ConductorPrivado import ConductorPrivado
from models.Vehiculo import Vehiculo
from models.Unidad import Unidad

from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from services.github_repo_service import upload_image
from schemas.ConductorScheme import ConductorEmpresaCreate, ConductorPrivadoCreate

async def conductor_empresa_create(
    conductor: ConductorEmpresaCreate,
    fotoperfil: Optional[UploadFile],
    licenciafrontal: UploadFile,
    licenciareverso: UploadFile,
    db: Session):

    usuario = db.query(Usuario).filter_by(id_usuario=conductor.id_usuario).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="User not found")
    
    isConductor = db.query(Conductor).filter_by(id_usuario=conductor.id_usuario).first()

    if isConductor:
        raise HTTPException(status_code=400, detail="Driver already exist")
    
    isConductorEmpresa = db.query(ConductorEmpresa).filter_by(codigo_empleado=conductor.codigo_empleado).first()
    
    if isConductorEmpresa:
        raise HTTPException(status_code=400, detail="Employee code is already in use")
    
    # verificar que el codigo proporcionado exista y no este asignado (null) para asignarse
    isEmpleado = db.query(Empleado).filter_by(codigo_empleado=conductor.codigo_empleado, id_conductor_empresa=None).first()
    
    if not isEmpleado:
        raise HTTPException(status_code=400, detail="Code not available")

    # preparar imagenes, extraer extensiones y bytes

    if fotoperfil:
        fotoperfil_extension = Path(fotoperfil.filename).suffix.lower()
        fotoperfil = await fotoperfil.read()
    else:
        fotoperfil_extension = None
        fotoperfil = conductor.foto_perfil
    
    licencia_frontal_extension = Path(licenciafrontal.filename).suffix.lower()
    licenciafrontal = await licenciafrontal.read() if licenciafrontal else None

    licencia_reverso_extension = Path(licenciareverso.filename).suffix.lower()
    licenciareverso = await licenciareverso.read() if licenciareverso else None

    # verifica que se reciban las imagenes correspondientes
    if not fotoperfil or not licenciafrontal or not licenciareverso:
        raise HTTPException(status_code=400, detail="No data provided")
    
    try:
        # Subir y obtener url foto perfil del repositorio de github
        if not isinstance(fotoperfil, str):
            fotoperfil = await upload_image(image_bytes=fotoperfil, extension=fotoperfil_extension)

        # Subir y obtener url licencia frontal
        if licenciafrontal:
            licenciafrontal = await upload_image(image_bytes=licenciafrontal, extension=licencia_frontal_extension)

        # Subir y obtener url licencia reverso
        if licenciareverso:
            licenciareverso = await upload_image(image_bytes=licenciareverso, extension=licencia_reverso_extension)

        #verifica que las imagenes se hayan subido correctamente
        if not fotoperfil or not licenciafrontal or not licenciareverso:
            raise HTTPException(status_code=400, detail="No data provided")
        
        # Actualiza los datos del usuario
        usuario.nombres = conductor.nombre
        usuario.apellidos = conductor.apellido
        usuario.fecha_nacimiento = conductor.fecha_nacimiento
        usuario.foto_perfil = fotoperfil
        db.commit()

        # Inserta un conductor
        new_conductor = Conductor(
            id_usuario = usuario.id_usuario,
            tipo_conductor = "EMPRESA",
            numero_licencia = conductor.numero_licencia,
            fecha_vencimiento = conductor.fecha_vencimiento,
            licencia_frontal = licenciafrontal,
            licencia_reverso = licenciareverso,
            id_unidad = None,
            id_ruta = None
        )

        db.add(new_conductor)
        db.commit()
        db.refresh(new_conductor)

        # Insertar conductor de empresa
        new_conductor_empresa = ConductorEmpresa(
            id_conductor=new_conductor.id_conductor,
            codigo_empleado=conductor.codigo_empleado
        )

        db.add(new_conductor_empresa)
        db.commit()
        db.refresh(new_conductor_empresa)

        # vincular cuenta de empleado con conductor empresa
        isEmpleado.id_conductor_empresa = new_conductor_empresa.id_conductor_empresa
        db.commit()

        return JSONResponse(content={
            "details": "OK"
        }, status_code=200)
    
    except  Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
    



async def conductor_privado_create(
    conductor: ConductorPrivadoCreate,
    fotoperfil: Optional[UploadFile],
    licenciafrontal: UploadFile,
    licenciareverso: UploadFile,
    db: Session):

    usuario = db.query(Usuario).filter_by(id_usuario=conductor.id_usuario).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="User not found")
    
    isConductor = db.query(Conductor).filter_by(id_usuario=conductor.id_usuario).first()

    if isConductor:
        raise HTTPException(status_code=400, detail="Driver already exist")
    
    
    # mas validaciones ...


    # preparar imagenes, extraer extensiones y bytes

    if fotoperfil:
        fotoperfil_extension = Path(fotoperfil.filename).suffix.lower()
        fotoperfil = await fotoperfil.read()
    else:
        fotoperfil_extension = None
        fotoperfil = conductor.foto_perfil
    
    licencia_frontal_extension = Path(licenciafrontal.filename).suffix.lower()
    licenciafrontal = await licenciafrontal.read() if licenciafrontal else None

    licencia_reverso_extension = Path(licenciareverso.filename).suffix.lower()
    licenciareverso = await licenciareverso.read() if licenciareverso else None

    # verifica que se reciban las imagenes correspondientes
    if not fotoperfil or not licenciafrontal or not licenciareverso:
        raise HTTPException(status_code=400, detail="No data provided")
    
    try:
        # Subir y obtener url foto perfil del repositorio de github
        if not isinstance(fotoperfil, str):
            fotoperfil = await upload_image(image_bytes=fotoperfil, extension=fotoperfil_extension)

        # Subir y obtener url licencia frontal
        if licenciafrontal:
            licenciafrontal = await upload_image(image_bytes=licenciafrontal, extension=licencia_frontal_extension)

        # Subir y obtener url licencia reverso
        if licenciareverso:
            licenciareverso = await upload_image(image_bytes=licenciareverso, extension=licencia_reverso_extension)

        #verifica que las imagenes se hayan subido correctamente
        if not fotoperfil or not licenciafrontal or not licenciareverso:
            raise HTTPException(status_code=400, detail="No data provided")
        
        # Actualiza los datos del usuario
        usuario.nombres = conductor.nombre
        usuario.apellidos = conductor.apellido
        usuario.fecha_nacimiento = conductor.fecha_nacimiento
        usuario.foto_perfil = fotoperfil
        db.commit()


        # Inserta un conductor
        new_conductor = Conductor(
            id_usuario = usuario.id_usuario,
            tipo_conductor = "PRIVADO",
            numero_licencia = conductor.numero_licencia,
            fecha_vencimiento = conductor.fecha_vencimiento,
            licencia_frontal = licenciafrontal,
            licencia_reverso = licenciareverso,
            id_unidad = None,
            id_ruta = None
        )

        db.add(new_conductor)
        db.commit()
        db.refresh(new_conductor)

        
        # Insertar y vincular conductor privado
        new_conductor_privado = ConductorPrivado(
            id_conductor=new_conductor.id_conductor
        )

        db.add(new_conductor_privado)
        db.commit()
        db.refresh(new_conductor_privado)

        
        # Inserta un vehiculo
        new_vehiculo = Vehiculo(
            placa = conductor.numero_placa,
            marca = conductor.marca_vehiculo,
            modelo = conductor.modelo_vehiculo,
            color = conductor.color_vehiculo
        )

        db.add(new_vehiculo)
        db.commit()
        db.refresh(new_vehiculo)

        # Inserta una unidad y vincula con vehiculo y propietario

        new_unidad = Unidad(
            id_propietario = new_conductor_privado.id_conductor_privado, # empresa o conductor privado
            tipo_propietario = "P", # privado
            numero = 1, # unico
            id_vehiculo = new_vehiculo.id_vehiculo,
            id_transporte = 1 #colectivo
        )

        db.add(new_unidad)
        db.commit()
        db.refresh(new_unidad)

        new_conductor.id_unidad = new_unidad.id_unidad
        db.commit()

        return JSONResponse(content={
            "details": "OK"
        }, status_code=200)
    
    except  Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")