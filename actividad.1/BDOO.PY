from persistent import Persistent
from persistent.mapping import PersistentMapping
from ZODB import DB
from ZODB.FileStorage import FileStorage
import transaction


class Persona(Persistent):
    """Clase base que representa una persona."""

    def __init__(self, nombre, edad, correo):
        self.nombre = nombre
        self.edad = edad
        self.correo = correo

    def mostrar_datos(self):
        return f"Nombre: {self.nombre} | Edad: {self.edad} | Correo: {self.correo}"


class Estudiante(Persona):
    """Estudiante hereda los atributos y metodos de Persona."""

    def __init__(self, matricula, nombre, edad, correo, carrera):
        super().__init__(nombre, edad, correo)
        self.matricula = matricula
        self.carrera = carrera

    def mostrar_datos(self):
        return (
            f"Matricula: {self.matricula} | {super().mostrar_datos()} | "
            f"Carrera: {self.carrera}"
        )


class BaseDatosEstudiantes:
    """Maneja la conexion y las operaciones CRUD de estudiantes."""

    def __init__(self, archivo="estudiantes.fs"):
        self.storage = FileStorage(archivo)
        self.db = DB(self.storage)
        self.conexion = self.db.open()
        self.raiz = self.conexion.root()

        if "estudiantes" not in self.raiz:
            self.raiz["estudiantes"] = PersistentMapping()
            transaction.commit()

    def crear(self, estudiante):
        if estudiante.matricula in self.raiz["estudiantes"]:
            return False

        self.raiz["estudiantes"][estudiante.matricula] = estudiante
        transaction.commit()
        return True

    def leer(self, matricula):
        return self.raiz["estudiantes"].get(matricula)

    def listar(self):
        return list(self.raiz["estudiantes"].values())

    def actualizar(self, matricula, nombre=None, edad=None, correo=None, carrera=None):
        estudiante = self.leer(matricula)
        if estudiante is None:
            return False

        if nombre:
            estudiante.nombre = nombre
        if edad is not None:
            estudiante.edad = edad
        if correo:
            estudiante.correo = correo
        if carrera:
            estudiante.carrera = carrera

        transaction.commit()
        return True

    def eliminar(self, matricula):
        if matricula not in self.raiz["estudiantes"]:
            return False

        del self.raiz["estudiantes"][matricula]
        transaction.commit()
        return True

    def cerrar(self):
        self.conexion.close()
        self.db.close()
        self.storage.close()


def pedir_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Ingresa un numero entero valido.")


def menu():
    bd = BaseDatosEstudiantes()

    try:
        while True:
            print("\n--- CRUD BDOO - ESTUDIANTES ---")
            print("1. Crear estudiante")
            print("2. Consultar estudiante")
            print("3. Mostrar todos")
            print("4. Actualizar estudiante")
            print("5. Eliminar estudiante")
            print("6. Salir")

            opcion = input("Selecciona una opcion: ").strip()

            if opcion == "1":
                matricula = input("Matricula: ").strip()
                nombre = input("Nombre: ").strip()
                edad = pedir_entero("Edad: ")
                correo = input("Correo: ").strip()
                carrera = input("Carrera: ").strip()

                estudiante = Estudiante(matricula, nombre, edad, correo, carrera)
                if bd.crear(estudiante):
                    print("Estudiante guardado correctamente.")
                else:
                    print("Ya existe un estudiante con esa matricula.")

            elif opcion == "2":
                matricula = input("Matricula a buscar: ").strip()
                estudiante = bd.leer(matricula)
                print(estudiante.mostrar_datos() if estudiante else "Estudiante no encontrado.")

            elif opcion == "3":
                estudiantes = bd.listar()
                if not estudiantes:
                    print("No hay estudiantes registrados.")
                else:
                    for estudiante in estudiantes:
                        print(estudiante.mostrar_datos())

            elif opcion == "4":
                matricula = input("Matricula a actualizar: ").strip()
                estudiante = bd.leer(matricula)

                if estudiante is None:
                    print("Estudiante no encontrado.")
                    continue

                print("Deja un campo vacio para conservar el valor actual.")
                nombre = input(f"Nombre [{estudiante.nombre}]: ").strip()
                edad_texto = input(f"Edad [{estudiante.edad}]: ").strip()
                correo = input(f"Correo [{estudiante.correo}]: ").strip()
                carrera = input(f"Carrera [{estudiante.carrera}]: ").strip()

                edad = int(edad_texto) if edad_texto else None
                bd.actualizar(matricula, nombre, edad, correo, carrera)
                print("Estudiante actualizado correctamente.")

            elif opcion == "5":
                matricula = input("Matricula a eliminar: ").strip()
                if bd.eliminar(matricula):
                    print("Estudiante eliminado correctamente.")
                else:
                    print("Estudiante no encontrado.")

            elif opcion == "6":
                print("Programa finalizado.")
                break

            else:
                print("Opcion no valida.")

    finally:
        bd.cerrar()


if __name__ == "__main__":
    menu()