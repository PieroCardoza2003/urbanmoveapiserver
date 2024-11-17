from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import UsuarioRoutes, VehiculoRoutes, PingRoute, EmpresaRoute, ConductorRoute

app = FastAPI()


# Lista de orígenes permitidos
origins = [
    "http://localhost",
    "http://localhost:3000",  # Si estás usando un frontend como React/Vue
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Orígenes permitidos
    allow_credentials=True,  # Permitir envío de cookies o credenciales
    allow_methods=["*"],  # Métodos HTTP permitidos (GET, POST, etc.)
    allow_headers=["*"],  # Encabezados permitidos
)

app.include_router(PingRoute.router, prefix="/api")

app.include_router(UsuarioRoutes.router, prefix="/api")
app.include_router(VehiculoRoutes.router, prefix="/api")
app.include_router(EmpresaRoute.router, prefix="/api")
app.include_router(ConductorRoute.router, prefix="/api")


@app.get("/")
def root():
    return { "message": "Home" }