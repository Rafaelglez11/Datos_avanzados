class Libro:

    def __init__(self, titulo, autor):
        self.titulo = titulo
        self.autor = autor
        self.disponible = True

    def prestar(self):
        if self.disponible:
            self.disponible = False
            print("Libro prestado correctamente.")
        else:
            print("El libro no está disponible.")

    def devolver(self):
        if not self.disponible:
            self.disponible = True
            print("Libro devuelto correctamente.")
        else:
            print("El libro ya estaba disponible.")

    def mostrar_estado(self):
        if self.disponible:
            print("Libro disponible.")
        else:
            print("Libro no disponible.")


libro = Libro(
    "Don Quijote de la Mancha",
    "Miguel de Cervantes"
)

libro.mostrar_estado()
libro.prestar()
libro.mostrar_estado()
libro.prestar()
libro.devolver()
libro.mostrar_estado()
