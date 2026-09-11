from biblioteca_zodb import BibliotecaDB


def main():
    biblioteca = BibliotecaDB("biblioteca.fs")

    try:
        # Registrar datos únicamente si todavía no existen.
        if "A001" not in biblioteca.root.autores:
            biblioteca.registrar_autor("A001", "Gabriel García Márquez", "Colombiana")

        if "9780307474728" not in biblioteca.root.libros:
            biblioteca.registrar_libro(
                "9780307474728",
                "Cien años de soledad",
                1967,
                "Literatura",
                2,
                ["A001"]
            )

        if "20260001" not in biblioteca.root.estudiantes:
            biblioteca.registrar_estudiante(
                "20260001",
                "Ana López",
                "Ingeniería en Inteligencia Artificial",
                "ana.lopez@universidad.edu"
            )

        print("\n1. LIBROS REGISTRADOS")
        for libro in biblioteca.consultar_libros():
            print(libro)

        isbn = "9780307474728"
        print("\n2. BÚSQUEDA POR ISBN")
        print(biblioteca.buscar_libro_isbn(isbn))
        print("Ejemplares disponibles:", biblioteca.ejemplares_disponibles(isbn))

        print("\n3. REGISTRAR PRÉSTAMO")
        prestamo = biblioteca.registrar_prestamo("20260001", isbn)
        print(prestamo)
        print("Ejemplares disponibles:", biblioteca.ejemplares_disponibles(isbn))

        print("\n4. PRÉSTAMOS DEL ESTUDIANTE")
        for p in biblioteca.consultar_prestamos_estudiante("20260001"):
            print(p)

        print("\n5. REGISTRAR DEVOLUCIÓN")
        biblioteca.registrar_devolucion(prestamo.id_prestamo)
        print("Estado:", prestamo.estado)
        print("Fecha real de devolución:", prestamo.fecha_real_devolucion)
        print("Ejemplares disponibles:", biblioteca.ejemplares_disponibles(isbn))

    except ValueError as error:
        print("Aviso:", error)
    finally:
        biblioteca.cerrar()


if __name__ == "__main__":
    main()
