class Libro:

    def __init__(self, titulo, autor, isbn, anio, editorial, categoria, numero_paginas, disponible=True):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.anio = anio
        self.editorial = editorial
        self.categoria = categoria
        self.numero_paginas = numero_paginas
        self.disponible = disponible


libro = Libro(
    "1984",
    "George Orwell",
    "9780451524935",
    1949,
    "Signet Classics",
    "Novela",
    328
)

print("Título:", libro.titulo)
print("Autor:", libro.autor)
print("ISBN:", libro.isbn)
print("Año:", libro.anio)
print("Editorial:", libro.editorial)
print("Categoría:", libro.categoria)
print("Número de páginas:", libro.numero_paginas)
print("Disponible:", libro.disponible)
