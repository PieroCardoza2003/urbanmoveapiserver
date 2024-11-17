from fastapi import FastAPI
from routes import UsuarioRoutes, VehiculoRoutes, PingRoute, EmpresaRoute, ConductorRoute

app = FastAPI()

app.include_router(PingRoute.router, prefix="/api")

app.include_router(UsuarioRoutes.router, prefix="/api")
app.include_router(VehiculoRoutes.router, prefix="/api")
app.include_router(EmpresaRoute.router, prefix="/api")
app.include_router(ConductorRoute.router, prefix="/api")


@app.get("/")
def root():
    return { "message": "Home" }