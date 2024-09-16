from fastapi import FastAPI
from routes import UsuarioRoutes

app = FastAPI()

app.include_router(UsuarioRoutes.router, prefix="/api")


@app.get("/")
def root():
    return { "message": "Home" }