from persistent import Persistent


class Recurso(Persistent):
    def __init__(self, id_recurso, nombre, tipo, costo, marca, modelo):
        self.id_recurso = id_recurso
        self.nombre = nombre
        self.tipo = tipo
        self.costo = costo
        self.marca = marca
        self.modelo = modelo
        self.disponible = True

    def prestar(self):
        if not self.disponible:
            return False

        self.disponible = False
        return True

    def devolver(self):
        self.disponible = True

    def esta_disponible(self):
        return self.disponible

    def mostrar_info(self):
        estado = "Disponible" if self.disponible else "Prestado"

        return (
            f"{self.id_recurso} - "
            f"{self.nombre} - "
            f"{self.tipo} - "
            f"${self.costo:,.2f} - "
            f"{self.marca} {self.modelo} - "
            f"{estado}"
        )


class Estudiante(Persistent):
    def __init__(self, matricula, nombre, carrera):
        self.matricula = matricula
        self.nombre = nombre
        self.carrera = carrera

    def mostrar_info(self):
        return f"{self.matricula} - {self.nombre} - {self.carrera}"


class Prestamo(Persistent):
    def __init__(self, id_prestamo, estudiante, recurso, fecha):
        self.id_prestamo = id_prestamo
        self.estudiante = estudiante
        self.recurso = recurso
        self.fecha = fecha
        self.activo = True

    def devolver(self):
        self.activo = False
        self.recurso.devolver()

    def esta_activo(self):
        return self.activo

    def mostrar_info(self):
        estado = "Activo" if self.activo else "Finalizado"

        return (
            f"{self.id_prestamo} - "
            f"{self.estudiante.nombre} - "
            f"{self.recurso.nombre} - "
            f"{self.fecha} - "
            f"{estado}"
        )
