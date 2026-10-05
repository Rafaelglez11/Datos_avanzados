from ZODB import DB
from ZODB.FileStorage import FileStorage
from persistent import Persistent
from persistent.list import PersistentList
import transaction


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

autor1 = Autor("George Orwell")
autor2 = Autor("Gabriel García Márquez")
autor3 = Autor("Carlos Ruiz Zafón")

libro1 = Libro("1984", "9780451524935", autor1, 1949, "Signet Classics", "Novela", 328)
libro2 = Libro("Rebelión en la granja", "9780451526342", autor1, 1945, "Signet Classics", "Novela", 144)
libro3 = Libro("Cien años de soledad", "9780307474728", autor2, 1967, "Vintage Español", "Realismo mágico", 496)
libro4 = Libro("El amor en los tiempos del cólera", "9780307389732", autor2, 1985, "Vintage Español", "Novela", 368)
libro5 = Libro("La sombra del viento", "9788408172178", autor3, 2001, "Planeta", "Misterio", 576)

autor1.libros.extend([libro1, libro2])
autor2.libros.extend([libro3, libro4])
autor3.libros.append(libro5)

usuario1 = Usuario("Ana López", "U001")
usuario2 = Usuario("Carlos Pérez", "U002")
usuario3 = Usuario("María Hernández", "U003")

prestamo1 = Prestamo(usuario1, libro1, "2026-10-01")
prestamo2 = Prestamo(usuario2, libro3, "2026-10-02")

usuario1.prestamos.append(prestamo1)
usuario2.prestamos.append(prestamo2)

libro1.disponible = False
libro3.disponible = False

root["autores"] = PersistentList([autor1, autor2, autor3])
root["libros"] = PersistentList([libro1, libro2, libro3, libro4, libro5])
root["usuarios"] = PersistentList([usuario1, usuario2, usuario3])
root["prestamos"] = PersistentList([prestamo1, prestamo2])

transaction.commit()

print("Datos guardados correctamente en biblioteca.fs")
print("Autores:", len(root["autores"]))
print("Libros:", len(root["libros"]))
print("Usuarios:", len(root["usuarios"]))
print("Préstamos:", len(root["prestamos"]))

connection.close()
db.close()
storage.close()
