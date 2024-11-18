from models.Empresa import Empresa
from models.Empleado import Empleado
from models.Vehiculo import Vehiculo
from models.Unidad import Unidad
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from utils.string_utils import is_blank
from utils.email_utils import verify_email
from utils.bcrypt_utils import encode_password, verify_password
from utils.randomcode_utils import generar_codigo_unico
from schemas.EmpresaScheme import EmpresaCreate, EmpleadoCreate, EmpresaLogin, UnidadCreate, EmpleadoResponse


def empresa_create(db: Session, empresa: EmpresaCreate):

    if not verify_email(empresa.email):
        raise HTTPException(status_code=400, detail="Invalid email")
    
    existing_empresa = db.query(Empresa).filter_by(email=empresa.email).first()

    if existing_empresa:
        raise HTTPException(status_code=400, detail="Company already exists")

    try:
        new_empresa = Empresa(
            razon_social=empresa.razon_social,
            ruc=empresa.ruc,
            direccion=empresa.direccion,
            telefono=empresa.telefono,
            email=empresa.email,
            password=encode_password(empresa.password)
        )

        db.add(new_empresa)
        db.commit()
        db.refresh(new_empresa)

        return new_empresa
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")


def empresa_get_all(db: Session):
    return db.query(Empresa).order_by(Empresa.razon_social).all()


def empleado_get_all(empresaID: str, db: Session):

    

    query = """
        SELECT e.codigo_empleado, 
            CONCAT(COALESCE(u.nombres, ''), ' ', COALESCE(u.apellidos, '')) as conductor, 
            e.fecha_registro 
        FROM empleado AS e
        LEFT JOIN conductor_empresa AS ce ON ce.id_conductor_empresa = e.id_conductor_empresa
        LEFT JOIN conductor AS c ON c.id_conductor = ce.id_conductor
        LEFT JOIN usuario AS u ON u.id_usuario = c.id_usuario
        where e.id_empresa = :empresaID;
        """
    
    result = db.execute(text(query), {'empresaID': empresaID}).fetchall()
    
    dict_data = [
        {
            "codigo_empleado": item[0],
            "conductor": item[1],
            "fecha_registro": item[2].strftime('%Y-%m-%d %H:%M:%S')  # Convertir datetime a cadena
        }
        for item in result
    ]

    return dict_data


def vehiculo_get_all(db: Session):
    return db.query(Vehiculo).all()


def unidad_get_all(db: Session):
    return db.query(Unidad).all()


def empleado_create(db: Session, empleado: EmpleadoCreate):

    existing_empresa = db.query(Empresa).filter_by(id_empresa = empleado.id_empresa).first()

    if not existing_empresa:
        raise HTTPException(status_code=404, detail="Company not found")
    
    try:
        new_empleado = Empleado(
            id_empresa=empleado.id_empresa,
            codigo_empleado=generar_codigo_unico()
        )

        db.add(new_empleado)
        db.commit()
        db.refresh(new_empleado)

        return new_empleado
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")


def empresa_login(db: Session, empresa: EmpresaLogin):
    empresa_email = empresa.email.strip()
    empresa_password = empresa.password.strip()

    if not verify_email(empresa_email) or is_blank(empresa_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    existing_empresa = db.query(Empresa).filter_by(email=empresa_email).first()
    
    if not existing_empresa or not verify_password(existing_empresa.password, empresa_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return JSONResponse(content={
            "id_empresa": str(existing_empresa.id_empresa)
        }, status_code=200)




def unidad_create(db: Session, unidad: UnidadCreate):
    try:
        existing_vehicle = db.query(Vehiculo).filter_by(placa = unidad.placa).first()

        if existing_vehicle:
            raise HTTPException(status_code=404, detail="Vehicle alredy exists")
    
        new_vehicle = Vehiculo(
            placa=unidad.placa,
            marca=unidad.marca,
            modelo=unidad.modelo,
            color=unidad.color
        )

        db.add(new_vehicle)
        db.commit()
        db.refresh(new_vehicle)

        new_unidad = Unidad(
            id_propietario=unidad.id_propietario,
            tipo_propietario=unidad.tipo_propietario,
            numero=unidad.numero,
            id_vehiculo=new_vehicle.id_vehiculo,
            id_transporte=unidad.id_transporte
        )

        db.add(new_unidad)
        db.commit()
        db.refresh(new_unidad)

        return JSONResponse(content={
            "details": "OK"
            }, status_code=200)
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")