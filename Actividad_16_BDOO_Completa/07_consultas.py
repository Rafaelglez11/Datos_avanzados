from ZODB import DB
from ZODB.FileStorage import FileStorage
from persistent import Persistent
from persistent.list import PersistentList


class Autor(Persistent):
    def __init__(self, nombre):
        self.nombre = nombre
        self.libros = PersistentList()


class Libro(Persistent):
    def __init__(self, titulo, isbn, autor, anio, editorial, categoria, numero_paginas):
        self.titulo = titulo
        self.isbn = isbn
        self.autor = autor
        self.anio = anio
        self.editorial = editorial
        self.categoria = categoria
        self.numero_paginas = numero_paginas
        self.disponible = True


class Usuario(Persistent):
    def __init__(self, nombre, matricula):
        self.nombre = nombre
        self.matricula = matricula
        self.prestamos = PersistentList()


class Prestamo(Persistent):
    def __init__(self, usuario, libro, fecha):
        self.usuario = usuario
        self.libro = libro
        self.fecha = fecha


storage = FileStorage("biblioteca.fs")
db = DB(storage)
connection = db.open()
root = connection.root()

if "libros" not in root:
    print("No hay libros cargados. Ejecuta primero 06_diseno_bdoo.py")
else:
    print("\n--- LIBROS ---")
    for libro in root["libros"]:
        print(libro.titulo, "-", libro.autor.nombre)

    titulo_buscar = "1984"
    print("\n--- BÚSQUEDA POR TÍTULO ---")

    encontrado = False
    for libro in root["libros"]:
        if libro.titulo.lower() == titulo_buscar.lower():
            print("Libro encontrado:", libro.titulo)
            print("Autor:", libro.autor.nombre)
            print("ISBN:", libro.isbn)
            encontrado = True
            break

    if not encontrado:
        print("Libro no encontrado.")

    print("\n--- LIBROS DISPONIBLES ---")
    for libro in root["libros"]:
        if libro.disponible:
            print(libro.titulo)

    print("\n--- LIBROS DESPUÉS DEL AÑO 2000 ---")
    for libro in root["libros"]:
        if libro.anio > 2000:
            print(libro.titulo, "-", libro.anio)

connection.close()
db.close()
storage.close()
