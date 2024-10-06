from fastapi import APIRouter, Response
from config.db import con
from modelos.user import users
from esquemas.user import User
from cryptography.fernet import Fernet
from starlette.status import HTTP_204_NO_CONTENT

# Api Router para pasar las rutas a app y usarlas
user = APIRouter()

# Cifrar para Guardar
key = b'WgWx8gKOnJZRjR-QAGzx9drg_XaN94FqZKqUhylItiU='
f = Fernet(key)

# Obtener todos los Usuarios
@user.get("/users", response_model=list[User])
def get_users():
    users_show = con.execute(users.select().order_by(users.c.id.asc())).fetchall()

    # Hacemos una List comprehesion
    users_list = [{"id": row.id, "name": row.name, "email": row.email} for row in users_show]
    return users_list

# Crear un nuevo usuario
@user.post("/users", response_model=User)
def create_user(user: User):
    # Encriptamos la contraseña
    pas_cifrada = f.encrypt(user.password.encode())
    print(pas_cifrada)

    # Agregarmos la data al esquema user y retornamos el id con returning
    add = users.insert().values(
        name = user.name,
        email = user.email,
        password = pas_cifrada
    ).returning(users.c.id)

    res = con.execute(add)
    con.commit()

    idn = res.fetchone()[0]

    # Hacemos un select con el id a extraer y lo hacemos un diccionario para retornar
    user_insert = con.execute(users.select().where(users.c.id == idn)).first() 
    user_dic = {
        "id": user_insert.id,
        "name": user_insert.name,
        "email": user_insert.email,
        "password": user_insert.password
    }
    print(user_dic)
    return user_dic

# Mostrar un usuario especifico
@user.get("/users/{id}", response_model=User)
def get_user(id: str):
    user_sel = con.execute(users.select().where(users.c.id == id)).first()

    if (user_sel == None):
        return "Usuario no econtrado"
    
    user_dic = {
        "id": user_sel.id,
        "name": user_sel.name,
        "email": user_sel.email,
        "password": user_sel.password
    }

    return user_dic

# Eliminar un usuario
@user.delete("/users/{id}", response_model=User)
def delete_user(id: str):
    user_sel = con.execute(users.select().where(users.c.id == id)).first()

    if (user_sel == None):
        return "Nada para Eliminar"
    
    con.execute(users.delete().where(users.c.id == id))
    con.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)

# Actualizar un usuario
@user.put("/users/{id}", response_model=User)
def update_user(id: str, user: User):
    pas_cifrada = f.encrypt(user.password.encode())

    # Ejecutar la actualización en la base de datos
    con.execute(users.update().values(
        name=user.name,
        email=user.email,
        password=pas_cifrada
    ).where(users.c.id == id))

    con.commit()

    usuario = get_user(id)
    return usuario


