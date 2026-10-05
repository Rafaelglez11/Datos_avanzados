class Libro:
    def __init__(self, titulo, autor, anio):
        self.titulo = titulo
        self.autor = autor
        self.anio = anio

    def mostrar_informacion(self):
        print("Título:", self.titulo)
        print("Autor:", self.autor)
        print("Año:", self.anio)
        print()


libro1 = Libro(
    "Cien años de soledad",
    "Gabriel García Márquez",
    1967
)

libro2 = Libro(
    "El principito",
    "Antoine de Saint-Exupéry",
    1943
)

libro3 = Libro(
    "1984",
    "George Orwell",
    1949
)

libros = [libro1, libro2, libro3]

for libro in libros:
    libro.mostrar_informacion()

print("Estado: son los valores que tiene un objeto en un momento determinado.")
print("Propiedades: son titulo, autor y anio.")
print("Comportamiento: es la acción mostrar_informacion().")
