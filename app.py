# Importar fastAPI y las rutas
from fastapi import FastAPI
from rutas.user import user

# Instanciar FastApi
app = FastAPI()

# Pasar las rutas
app.include_router(user)

