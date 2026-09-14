"""Persistencia con ZODB."""
from ZODB import DB, FileStorage
from persistent.mapping import PersistentMapping
import transaction

ARCHIVO_BD = "tienda.fs"
COLECCIONES = ("categorias", "proveedores", "productos", "clientes", "ventas")

def abrir_base_datos(ruta=ARCHIVO_BD):
    """Abre ZODB e inicializa las colecciones."""
    storage = FileStorage.FileStorage(ruta)
    db = DB(storage)
    conexion = db.open()
    raiz = conexion.root()
    for nombre in COLECCIONES:
        if nombre not in raiz:
            raiz[nombre] = PersistentMapping()
    transaction.commit()
    return storage, db, conexion, raiz

def guardar_cambios():
    """Guarda la transacción actual."""
    transaction.commit()

def cancelar_cambios():
    """Cancela la transacción actual."""
    transaction.abort()

def cerrar_base_datos(storage, db, conexion):
    """Cierra correctamente ZODB."""
    transaction.commit()
    conexion.close()
    db.close()
    storage.close()
