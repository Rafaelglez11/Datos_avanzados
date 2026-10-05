from ZODB import DB
from ZODB.FileStorage import FileStorage
import transaction


class Libro:
    def __init__(self, titulo, autor, anio):
        self.titulo = titulo
        self.autor = autor
        self.anio = anio


storage = FileStorage("biblioteca.fs")
db = DB(storage)
connection = db.open()
root = connection.root()

libro = Libro(
    "La sombra del viento",
    "Carlos Ruiz Zafón",
    2001
)

root["libro"] = libro
transaction.commit()

print("Libro almacenado correctamente.")

connection.close()
db.close()
storage.close()

storage = FileStorage("biblioteca.fs")
db = DB(storage)
connection = db.open()
root = connection.root()

libro_guardado = root["libro"]

print("\nLibro recuperado después de abrir nuevamente la base:")
print("Título:", libro_guardado.titulo)
print("Autor:", libro_guardado.autor)
print("Año:", libro_guardado.anio)

connection.close()
db.close()
storage.close()
