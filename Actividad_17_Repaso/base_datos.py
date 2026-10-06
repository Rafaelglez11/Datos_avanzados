import ZODB
import ZODB.FileStorage
import transaction

from persistent.mapping import PersistentMapping


def abrir_base_datos():
    storage = ZODB.FileStorage.FileStorage("laboratorio.fs")
    db = ZODB.DB(storage)
    connection = db.open()
    root = connection.root()

    return db, connection, root


def inicializar(root):
    if not hasattr(root, "recursos"):
        root.recursos = PersistentMapping()

    if not hasattr(root, "estudiantes"):
        root.estudiantes = PersistentMapping()

    if not hasattr(root, "prestamos"):
        root.prestamos = PersistentMapping()

    transaction.commit()


def cerrar_base_datos(db, connection):
    connection.close()
    db.close()
