from fastapi import FastAPI
from routes import UsuarioRoutes, VehiculoRoutes

app = FastAPI()

app.include_router(UsuarioRoutes.router, prefix="/api")
app.include_router(VehiculoRoutes.router, prefix="/api")


@app.get("/")
def root():
    return { "message": "Home" }