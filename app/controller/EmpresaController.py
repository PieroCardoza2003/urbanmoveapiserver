from models.Empresa import Empresa
from models.Empleado import Empleado
from models.Vehiculo import Vehiculo
from models.Unidad import Unidad
from models.TarifaRuta import TarifaRuta
from models.Ruta import Ruta
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from utils.string_utils import is_blank
from utils.email_utils import verify_email
from utils.bcrypt_utils import encode_password, verify_password
from utils.randomcode_utils import generar_codigo_unico
from schemas.EmpresaScheme import EmpresaCreate, EmpleadoCreate, EmpresaLogin, UnidadCreate, EmpleadoResponse, RutaCreate


def route_create(db: Session, route: RutaCreate):

    existing_empresa = db.query(Empresa).filter_by(id_empresa=route.id_empresa).first()

    if not existing_empresa:
        raise HTTPException(status_code=404, detail="Company not found")
    
    try:
        new_route = Ruta(
            id_empresa = route.id_empresa,
            letra_ruta = route.letra_ruta,
            horario = route.horario,
            id_transporte = route.id_transporte
        )
        db.add(new_route)
        db.commit()
        db.refresh(new_route)

        tarifas = [
            TarifaRuta(
                id_ruta=new_route.id_ruta,
                id_tarifa=tarifa.id_tarifa,
                precio=tarifa.precio
            )
            for tarifa in route.tarifas
        ]
        db.add_all(tarifas)
        db.commit()

        return JSONResponse(content={
            "details": "OK"
        }, status_code=200)
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")


def route_get_all(empresaID: str, db: Session):

    query = """
        select r.id_ruta, 
            r.letra_ruta as 
            ruta, r.horario, 
            t.nombre as transporte  
        FROM ruta as r
        INNER JOIN transporte as t ON t.id_transporte = r.id_transporte
        WHERE r.id_empresa = :empresaID;
    """

    result = db.execute(text(query), {'empresaID': empresaID}).fetchall()
    
    dict_data = [
        {
            "id_ruta": item[0],
            "ruta": item[1],
            "horario": item[2],
            "transporte": item[3]
        }
        for item in result
    ]

    return dict_data

def route_passenger_get_all(db: Session):
    query = """
        select r.id_ruta, r.letra_ruta, e.razon_social as empresa, t.id_transporte ,t.nombre as tipo_transporte from ruta as r
        INNER JOIN empresa as e ON e.id_empresa = r.id_empresa
        INNER JOIN transporte as t ON t.id_transporte = r.id_transporte;
    """
    result = db.execute(text(query)).fetchall()
    
    dict_data = [
        {
            "id_ruta": item[0],
            "letra_ruta": item[1],
            "empresa": item[2],
            "id_transporte": item[3],
            "tipo_transporte": item[4]
        }
        for item in result
    ]

    return dict_data


def route_driver_privado_get_all(db: Session):
    query = """
        select r.id_ruta, r.letra_ruta, e.razon_social as empresa, t.id_transporte ,t.nombre as tipo_transporte from ruta as r
        INNER JOIN empresa as e ON e.id_empresa = r.id_empresa
        INNER JOIN transporte as t ON t.id_transporte = r.id_transporte where t.id_transporte = 1;
    """
    result = db.execute(text(query)).fetchall()
    
    dict_data = [
        {
            "id_ruta": item[0],
            "letra_ruta": item[1],
            "empresa": item[2],
            "id_transporte": item[3],
            "tipo_transporte": item[4]
        }
        for item in result
    ]

    return dict_data



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
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")


def empresa_get_all(db: Session):
    return db.query(Empresa).order_by(Empresa.razon_social).all()


def empleado_get_all(empresaID: str, db: Session):
    query = """
        SELECT e.id_empleado, e.codigo_empleado, 
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
            "id_empleado": item[0],
            "codigo_empleado": item[1],
            "conductor": item[2],
            "fecha_registro": item[3].strftime('%Y-%m-%d %H:%M:%S')  # Convertir datetime a cadena
        }
        for item in result
    ]

    return dict_data


def vehiculo_get_all(db: Session):
    return db.query(Vehiculo).all()


def unidad_get_all(empresaID: str, db: Session):
    query = """
        select u.id_unidad, u.numero as 
         unidad, v.placa,
         CONCAT(COALESCE(v.marca, ''), ' ', COALESCE(v.modelo, '')) as vehiculo,
         t.nombre as tipo
        FROM unidad as u
            INNER JOIN vehiculo as v ON v.id_vehiculo = u.id_vehiculo
            INNER JOIN transporte as t ON t.id_transporte = u.id_transporte
        WHERE u.id_propietario = :empresaID;
    """

    result = db.execute(text(query), {'empresaID': empresaID}).fetchall()
    
    dict_data = [
        {
            "id_unidad": item[0],
            "unidad": item[1],
            "placa": item[2],
            "vehiculo": item[3],
            "tipo": item[4]
        }
        for item in result
    ]

    return dict_data


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
        db.rollback()
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
            tipo_propietario="E",
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