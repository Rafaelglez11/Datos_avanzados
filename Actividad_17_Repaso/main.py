import transaction
from datetime import date

from modelos import Recurso, Estudiante, Prestamo
from base_datos import abrir_base_datos, inicializar, cerrar_base_datos


def registrar_recurso(recursos, recurso):
    if recurso.id_recurso in recursos:
        print("Error: ya existe un recurso con ese identificador.")
        return False

    recursos[recurso.id_recurso] = recurso
    transaction.commit()
    print("Recurso registrado correctamente.")
    return True


def registrar_estudiante(estudiantes, estudiante):
    if estudiante.matricula in estudiantes:
        print("Error: ya existe un estudiante con esa matrícula.")
        return False

    estudiantes[estudiante.matricula] = estudiante
    transaction.commit()
    print("Estudiante registrado correctamente.")
    return True


def crear_datos_iniciales(root):
    if len(root.recursos) == 0:
        recursos = [
            Recurso(1, "NVIDIA RTX 4090", "GPU", 45000, "NVIDIA", "RTX 4090"),
            Recurso(2, "Jetson Orin", "Kit IA", 25000, "NVIDIA", "Jetson Orin"),
            Recurso(3, "Robot móvil", "Robot", 18000, "TurtleBot", "Burger"),
            Recurso(4, "Sensor LiDAR", "Sensor", 32000, "RPLIDAR", "A2"),
            Recurso(5, "Servidor IA", "Servidor", 85000, "Dell", "PowerEdge")
        ]

        for recurso in recursos:
            root.recursos[recurso.id_recurso] = recurso

    if len(root.estudiantes) == 0:
        estudiantes = [
            Estudiante("A001", "Ana López", "Ingeniería en IA"),
            Estudiante("A002", "Carlos Pérez", "Ingeniería en IA"),
            Estudiante("A003", "María Hernández", "Ingeniería en IA")
        ]

        for estudiante in estudiantes:
            root.estudiantes[estudiante.matricula] = estudiante

    transaction.commit()


def mostrar_recursos(root):
    print("\n--- Todos los recursos ---")

    if not root.recursos:
        print("No hay recursos registrados.")
        return

    for recurso in root.recursos.values():
        print(recurso.mostrar_info())


def buscar_recurso(root):
    try:
        id_buscar = int(input("ID del recurso: "))
    except ValueError:
        print("El ID debe ser un número.")
        return

    recurso = root.recursos.get(id_buscar)

    if recurso:
        print(recurso.mostrar_info())
    else:
        print("Recurso no encontrado.")


def recursos_disponibles(root):
    print("\n--- Recursos disponibles ---")

    encontrados = False

    for recurso in root.recursos.values():
        if recurso.esta_disponible():
            print(recurso.mostrar_info())
            encontrados = True

    if not encontrados:
        print("No hay recursos disponibles.")


def recursos_por_tipo(root):
    tipo = input("Tipo de recurso: ").strip().lower()

    print("\n--- Recursos por tipo ---")

    encontrados = False

    for recurso in root.recursos.values():
        if recurso.tipo.lower() == tipo:
            print(recurso.mostrar_info())
            encontrados = True

    if not encontrados:
        print("No se encontraron recursos de ese tipo.")


def recursos_por_fabricante(root):
    marca = input("Fabricante o marca: ").strip().lower()

    print("\n--- Recursos por fabricante ---")

    encontrados = False

    for recurso in root.recursos.values():
        if recurso.marca.lower() == marca:
            print(recurso.mostrar_info())
            encontrados = True

    if not encontrados:
        print("No se encontraron recursos de esa marca.")


def prestamos_activos(root):
    print("\n--- Préstamos activos ---")

    encontrados = False

    for prestamo in root.prestamos.values():
        if prestamo.esta_activo():
            print(
                f"Estudiante: {prestamo.estudiante.nombre} | "
                f"Recurso: {prestamo.recurso.nombre} | "
                f"Fecha: {prestamo.fecha}"
            )
            encontrados = True

    if not encontrados:
        print("No hay préstamos activos.")


def navegacion_objetos(root):
    print("\n--- Navegación entre objetos ---")

    if not root.prestamos:
        print("No hay préstamos registrados.")
        return

    for prestamo in root.prestamos.values():
        print(
            f"{prestamo.estudiante.nombre} -> "
            f"{prestamo.recurso.nombre}"
        )


def consulta_dos_condiciones(root):
    print("\n--- GPU con costo mayor a $20,000 ---")

    encontrados = False

    for recurso in root.recursos.values():
        if recurso.tipo.lower() == "gpu" and recurso.costo > 20000:
            print(recurso.mostrar_info())
            encontrados = True

    if not encontrados:
        print("No se encontraron recursos.")


def consulta_estadistica(root):
    total = len(root.recursos)

    disponibles = sum(
        1
        for recurso in root.recursos.values()
        if recurso.esta_disponible()
    )

    prestados = total - disponibles

    valor_total = sum(
        recurso.costo
        for recurso in root.recursos.values()
    )

    print("\n--- Estadísticas ---")
    print(f"Número total de recursos: {total}")
    print(f"Número de recursos disponibles: {disponibles}")
    print(f"Número de recursos prestados: {prestados}")
    print(f"Valor total de los recursos: ${valor_total:,.2f}")


def consulta_propia(root):
    print("\n--- Consulta propia ---")
    print("Préstamos activos de estudiantes de Ingeniería en IA con recursos NVIDIA")

    encontrados = False

    for prestamo in root.prestamos.values():
        if (
            prestamo.esta_activo()
            and prestamo.estudiante.carrera.lower() == "ingeniería en ia"
            and prestamo.recurso.marca.lower() == "nvidia"
        ):
            print(
                f"{prestamo.estudiante.nombre} -> "
                f"{prestamo.recurso.nombre}"
            )
            encontrados = True

    if not encontrados:
        print("No hay préstamos que cumplan la condición.")


def nuevo_recurso(root):
    try:
        id_recurso = int(input("ID: "))
        nombre = input("Nombre: ")
        tipo = input("Tipo: ")
        costo = float(input("Costo: "))
        marca = input("Marca: ")
        modelo = input("Modelo: ")

        recurso = Recurso(
            id_recurso,
            nombre,
            tipo,
            costo,
            marca,
            modelo
        )

        registrar_recurso(root.recursos, recurso)

    except ValueError:
        print("ID y costo deben ser valores numéricos.")


def nuevo_estudiante(root):
    matricula = input("Matrícula: ")
    nombre = input("Nombre: ")
    carrera = input("Carrera: ")

    estudiante = Estudiante(
        matricula,
        nombre,
        carrera
    )

    registrar_estudiante(
        root.estudiantes,
        estudiante
    )


def registrar_prestamo(root):
    try:
        id_prestamo = int(input("ID del préstamo: "))
    except ValueError:
        print("El ID debe ser numérico.")
        return

    if id_prestamo in root.prestamos:
        print("Ya existe un préstamo con ese ID.")
        return

    matricula = input("Matrícula del estudiante: ")

    estudiante = root.estudiantes.get(matricula)

    if not estudiante:
        print("Estudiante no encontrado.")
        return

    try:
        id_recurso = int(input("ID del recurso: "))
    except ValueError:
        print("El ID del recurso debe ser numérico.")
        return

    recurso = root.recursos.get(id_recurso)

    if not recurso:
        print("Recurso no encontrado.")
        return

    if not recurso.esta_disponible():
        print("El recurso no está disponible.")
        return

    if not recurso.prestar():
        print("No fue posible prestar el recurso.")
        return

    fecha = str(date.today())

    prestamo = Prestamo(
        id_prestamo,
        estudiante,
        recurso,
        fecha
    )

    root.prestamos[id_prestamo] = prestamo

    transaction.commit()

    print("Préstamo registrado correctamente.")


def devolver_recurso(root):
    try:
        id_prestamo = int(input("ID del préstamo: "))
    except ValueError:
        print("El ID debe ser numérico.")
        return

    prestamo = root.prestamos.get(id_prestamo)

    if not prestamo:
        print("Préstamo no encontrado.")
        return

    if not prestamo.esta_activo():
        print("El préstamo ya fue finalizado.")
        return

    prestamo.devolver()
    transaction.commit()

    print("Recurso devuelto correctamente.")


def mostrar_estudiantes(root):
    print("\n--- Estudiantes ---")

    for estudiante in root.estudiantes.values():
        print(estudiante.mostrar_info())


def mostrar_prestamos(root):
    print("\n--- Todos los préstamos ---")

    if not root.prestamos:
        print("No hay préstamos registrados.")
        return

    for prestamo in root.prestamos.values():
        print(prestamo.mostrar_info())


def menu():
    db, connection, root = abrir_base_datos()
    inicializar(root)
    crear_datos_iniciales(root)

    while True:
        print("""
==============================
 LABORATORIO - BDOO CON ZODB
==============================

1. Mostrar todos los recursos
2. Buscar recurso por ID
3. Mostrar recursos disponibles
4. Buscar recursos por tipo
5. Buscar recursos por fabricante
6. Mostrar préstamos activos
7. Navegación entre objetos
8. Consulta con dos condiciones
9. Consulta estadística
10. Consulta propia

11. Registrar recurso
12. Registrar estudiante
13. Registrar préstamo
14. Devolver recurso
15. Mostrar estudiantes
16. Mostrar todos los préstamos

0. Salir
""")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            mostrar_recursos(root)

        elif opcion == "2":
            buscar_recurso(root)

        elif opcion == "3":
            recursos_disponibles(root)

        elif opcion == "4":
            recursos_por_tipo(root)

        elif opcion == "5":
            recursos_por_fabricante(root)

        elif opcion == "6":
            prestamos_activos(root)

        elif opcion == "7":
            navegacion_objetos(root)

        elif opcion == "8":
            consulta_dos_condiciones(root)

        elif opcion == "9":
            consulta_estadistica(root)

        elif opcion == "10":
            consulta_propia(root)

        elif opcion == "11":
            nuevo_recurso(root)

        elif opcion == "12":
            nuevo_estudiante(root)

        elif opcion == "13":
            registrar_prestamo(root)

        elif opcion == "14":
            devolver_recurso(root)

        elif opcion == "15":
            mostrar_estudiantes(root)

        elif opcion == "16":
            mostrar_prestamos(root)

        elif opcion == "0":
            cerrar_base_datos(db, connection)
            print("Programa finalizado.")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()
