from sqlalchemy import create_engine, MetaData

# Crear una metadata
metadata = MetaData()

# Crear la Conexión
engine = create_engine('postgresql://postgres:EstebanSahidBD@localhost/storedb')

# Conectar a la Base
con = engine.connect()
