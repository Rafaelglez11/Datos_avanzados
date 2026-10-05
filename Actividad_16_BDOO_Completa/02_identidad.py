class Libro:
    def __init__(self, titulo, autor):
        self.titulo = titulo
        self.autor = autor


libro1 = Libro(
    "El principito",
    "Antoine de Saint-Exupéry"
)

libro2 = Libro(
    "El principito",
    "Antoine de Saint-Exupéry"
)

print("Libro 1:")
print(id(libro1))

print("\nLibro 2:")
print(id(libro2))

print("\n¿libro1 == libro2?")
print(libro1 == libro2)

libro1.titulo = "El principito - edición especial"

print("\nPropiedades de libro1:")
print("Título:", libro1.titulo)
print("Autor:", libro1.autor)

print("\nPropiedades de libro2:")
print("Título:", libro2.titulo)
print("Autor:", libro2.autor)
