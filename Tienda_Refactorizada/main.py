"""Aplicación de consola."""
from consultas import todos_los_productos, productos_bajo_stock, productos_por_proveedor, total_ventas, venta_total_diaria
from logica_negocio import registrar_categoria, registrar_proveedor, registrar_cliente, registrar_producto, modificar_precio_producto, incrementar_inventario, eliminar_producto, asociar_producto_proveedor, registrar_venta
from persistencia import abrir_base_datos, cerrar_base_datos

TITULO_SISTEMA = "TIENDA LA ECONÓMICA"

def imprimir_productos(productos):
    """Imprime productos sin duplicar código."""
    if not productos:
        print("No se encontraron productos.")
    for producto in productos:
        print(producto)

def mostrar_menu():
    """Muestra el menú principal."""
    print("\n" + "=" * 35)
    print(TITULO_SISTEMA)
    print("=" * 35)
    print("1. Registrar categoría")
    print("2. Registrar proveedor")
    print("3. Registrar cliente")
    print("4. Registrar producto")
    print("5. Mostrar productos")
    print("6. Modificar precio")
    print("7. Incrementar existencias")
    print("8. Eliminar producto")
    print("9. Asociar producto a proveedor")
    print("10. Registrar venta")
    print("11. Productos bajo stock")
    print("12. Productos por proveedor")
    print("13. Total de ventas")
    print("14. Venta total diaria")
    print("0. Salir")

def ejecutar_opcion(opcion, raiz):
    """Ejecuta la opción elegida."""
    if opcion == "1":
        registrar_categoria(raiz, input("ID: "), input("Nombre: "), input("Descripción: "))
    elif opcion == "2":
        registrar_proveedor(raiz, input("ID: "), input("Nombre: "), input("Teléfono: "), input("Correo: "), input("Dirección: "))
    elif opcion == "3":
        registrar_cliente(raiz, input("ID: "), input("Nombre: "), input("Teléfono: "), input("Correo: "))
    elif opcion == "4":
        registrar_producto(raiz, input("Código: "), input("Nombre: "), input("Descripción: "), input("Precio: "), input("Existencias: "), input("ID categoría: "))
    elif opcion == "5":
        imprimir_productos(todos_los_productos(raiz))
    elif opcion == "6":
        print(modificar_precio_producto(raiz, input("Código: "), input("Nuevo precio: ")))
    elif opcion == "7":
        print(incrementar_inventario(raiz, input("Código: "), input("Cantidad: ")))
    elif opcion == "8":
        print("Eliminado:", eliminar_producto(raiz, input("Código: ")).codigo)
    elif opcion == "9":
        asociar_producto_proveedor(raiz, input("ID proveedor: "), input("Código: "))
        print("Producto asociado.")
    elif opcion == "10":
        id_venta = input("ID venta: ")
        id_cliente = input("ID cliente: ")
        productos = []
        while True:
            codigo = input("Código producto (0 termina): ")
            if codigo == "0":
                break
            productos.append((codigo, input("Cantidad: ")))
        venta = registrar_venta(raiz, id_venta, id_cliente, productos)
        print(f"Venta registrada. Total: ${venta.calcular_total():.2f}")
    elif opcion == "11":
        imprimir_productos(productos_bajo_stock(raiz, input("Límite: ")))
    elif opcion == "12":
        imprimir_productos(productos_por_proveedor(raiz, input("ID proveedor: ")))
    elif opcion == "13":
        print(f"Total de ventas: ${total_ventas(raiz):.2f}")
    elif opcion == "14":
        reporte = venta_total_diaria(raiz)
        print(f"Fecha: {reporte['fecha']}")
        print(f"Ventas: {reporte['cantidad_ventas']}")
        print(f"Total del día: ${reporte['total']:.2f}")
    else:
        print("Opción no válida.")

def main():
    """Inicia la aplicación."""
    storage, db, conexion, raiz = abrir_base_datos()
    try:
        while True:
            mostrar_menu()
            opcion = input("Opción: ").strip()
            if opcion == "0":
                break
            try:
                ejecutar_opcion(opcion, raiz)
            except ValueError as error:
                print("Error:", error)
            except Exception as error:
                print("Error inesperado:", error)
    finally:
        cerrar_base_datos(storage, db, conexion)

if __name__ == "__main__":
    main()
