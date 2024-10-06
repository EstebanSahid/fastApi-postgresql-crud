# Exportar la Tabla, Columnas, tipos y la configuracion de BD
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import metadata, engine

# Tabla de usuarios a crear
users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100)),
    Column("email", String(100)),
    Column("password", String(255))
)

# Crear todas las tablas
metadata.create_all(engine)