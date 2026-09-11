from datetime import date, timedelta

import transaction
import ZODB
import ZODB.FileStorage
from persistent import Persistent
from persistent.mapping import PersistentMapping


class Autor(Persistent):
    def __init__(self, id_autor, nombre, nacionalidad=""):
        self.id_autor = id_autor
        self.nombre = nombre
        self.nacionalidad = nacionalidad

    def __str__(self):
        return f"{self.id_autor} - {self.nombre}"


class Libro(Persistent):
    def __init__(self, isbn, titulo, anio_publicacion, categoria,
                 numero_ejemplares, autores=None):
        self.isbn = isbn
        self.titulo = titulo
        self.anio_publicacion = anio_publicacion
        self.categoria = categoria
        self.numero_ejemplares = numero_ejemplares
        self.autores = autores or []

    def ejemplares_disponibles(self, prestamos_activos):
        return self.numero_ejemplares - prestamos_activos

    def esta_disponible(self, prestamos_activos):
        return self.ejemplares_disponibles(prestamos_activos) > 0

    def __str__(self):
        return f"{self.isbn} - {self.titulo} ({self.categoria})"


class Estudiante(Persistent):
    def __init__(self, matricula, nombre, carrera, correo):
        self.matricula = matricula
        self.nombre = nombre
        self.carrera = carrera
        self.correo = correo

    def __str__(self):
        return f"{self.matricula} - {self.nombre}"


class Prestamo(Persistent):
    def __init__(self, id_prestamo, matricula, isbn,
                 fecha_prestamo, fecha_limite):
        self.id_prestamo = id_prestamo
        self.matricula = matricula
        self.isbn = isbn
        self.fecha_prestamo = fecha_prestamo
        self.fecha_limite_devolucion = fecha_limite
        self.fecha_real_devolucion = None
        self.estado = "Activo"

    def registrar_devolucion(self, fecha_devolucion=None):
        if self.estado == "Devuelto":
            raise ValueError("El préstamo ya fue devuelto.")
        self.fecha_real_devolucion = fecha_devolucion or date.today()
        self.estado = "Devuelto"

    def __str__(self):
        return (
            f"Préstamo {self.id_prestamo} | Estudiante: {self.matricula} | "
            f"ISBN: {self.isbn} | Estado: {self.estado}"
        )


class BibliotecaDB:
    def __init__(self, archivo="biblioteca.fs"):
        self.storage = ZODB.FileStorage.FileStorage(archivo)
        self.db = ZODB.DB(self.storage)
        self.conexion = self.db.open()
        self.root = self.conexion.root()

        if "autores" not in self.root:
            self.root.autores = PersistentMapping()
        if "libros" not in self.root:
            self.root.libros = PersistentMapping()
        if "estudiantes" not in self.root:
            self.root.estudiantes = PersistentMapping()
        if "prestamos" not in self.root:
            self.root.prestamos = PersistentMapping()
        if "siguiente_prestamo" not in self.root:
            self.root.siguiente_prestamo = 1
        transaction.commit()

    def cerrar(self):
        self.conexion.close()
        self.db.close()
        self.storage.close()

    # ---------- Altas ----------
    def registrar_autor(self, id_autor, nombre, nacionalidad=""):
        if id_autor in self.root.autores:
            raise ValueError("Ya existe un autor con ese ID.")
        autor = Autor(id_autor, nombre, nacionalidad)
        self.root.autores[id_autor] = autor
        transaction.commit()
        return autor

    def registrar_libro(self, isbn, titulo, anio, categoria,
                        numero_ejemplares, autores=None):
        if isbn in self.root.libros:
            raise ValueError("Ya existe un libro con ese ISBN.")
        if numero_ejemplares <= 0:
            raise ValueError("El número de ejemplares debe ser mayor que cero.")

        autores = autores or []
        for id_autor in autores:
            if id_autor not in self.root.autores:
                raise ValueError(f"No existe el autor {id_autor}.")

        libro = Libro(isbn, titulo, anio, categoria,
                      numero_ejemplares, autores)
        self.root.libros[isbn] = libro
        transaction.commit()
        return libro

    def registrar_estudiante(self, matricula, nombre, carrera, correo):
        if matricula in self.root.estudiantes:
            raise ValueError("Ya existe un estudiante con esa matrícula.")
        estudiante = Estudiante(matricula, nombre, carrera, correo)
        self.root.estudiantes[matricula] = estudiante
        transaction.commit()
        return estudiante

    # ---------- Consultas ----------
    def consultar_libros(self):
        return list(self.root.libros.values())

    def buscar_libro_isbn(self, isbn):
        return self.root.libros.get(isbn)

    def prestamos_activos_libro(self, isbn):
        return sum(
            1 for prestamo in self.root.prestamos.values()
            if prestamo.isbn == isbn and prestamo.estado == "Activo"
        )

    def libro_disponible(self, isbn):
        libro = self.buscar_libro_isbn(isbn)
        if libro is None:
            return False
        activos = self.prestamos_activos_libro(isbn)
        return libro.esta_disponible(activos)

    def ejemplares_disponibles(self, isbn):
        libro = self.buscar_libro_isbn(isbn)
        if libro is None:
            return 0
        activos = self.prestamos_activos_libro(isbn)
        return libro.ejemplares_disponibles(activos)

    def consultar_prestamos_estudiante(self, matricula):
        return [
            p for p in self.root.prestamos.values()
            if p.matricula == matricula
        ]

    # ---------- Préstamos y devoluciones ----------
    def registrar_prestamo(self, matricula, isbn, dias=7):
        if matricula not in self.root.estudiantes:
            raise ValueError("El estudiante no está registrado.")
        if isbn not in self.root.libros:
            raise ValueError("El libro no está registrado.")
        if not self.libro_disponible(isbn):
            raise ValueError("No hay ejemplares disponibles de este libro.")

        id_prestamo = self.root.siguiente_prestamo
        fecha_prestamo = date.today()
        fecha_limite = fecha_prestamo + timedelta(days=dias)

        prestamo = Prestamo(
            id_prestamo, matricula, isbn,
            fecha_prestamo, fecha_limite
        )
        self.root.prestamos[id_prestamo] = prestamo
        self.root.siguiente_prestamo += 1
        transaction.commit()
        return prestamo

    def registrar_devolucion(self, id_prestamo):
        prestamo = self.root.prestamos.get(id_prestamo)
        if prestamo is None:
            raise ValueError("No existe ese préstamo.")
        prestamo.registrar_devolucion()
        transaction.commit()
        return prestamo
