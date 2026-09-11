from persistent import Persistent
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping
from ZODB import DB, FileStorage
import transaction
from datetime import datetime


class Categoria(Persistent):
    def __init__(self, id_categoria, nombre, descripcion=""):
        self.id_categoria = id_categoria
        self.nombre = nombre
        self.descripcion = descripcion

    def __str__(self):
        return f"{self.id_categoria} - {self.nombre}"


class Proveedor(Persistent):
    def __init__(self, id_proveedor, nombre, telefono="", correo="", direccion=""):
        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion
        self.productos = PersistentList()

    def agregar_producto(self, codigo_producto):
        if codigo_producto not in self.productos:
            self.productos.append(codigo_producto)

    def quitar_producto(self, codigo_producto):
        if codigo_producto in self.productos:
            self.productos.remove(codigo_producto)

    def __str__(self):
        return f"{self.id_proveedor} - {self.nombre}"


class Producto(Persistent):
    def __init__(self, codigo, nombre, descripcion, precio, existencias, categoria):
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = float(precio)
        self.existencias = int(existencias)
        self.categoria = categoria

    def incrementar_existencias(self, cantidad):
        self.existencias += int(cantidad)

    def disminuir_existencias(self, cantidad):
        cantidad = int(cantidad)
        if cantidad <= self.existencias:
            self.existencias -= cantidad
            return True
        return False

    def verificar_disponibilidad(self, cantidad=1):
        return self.existencias >= int(cantidad)

    def actualizar_precio(self, nuevo_precio):
        self.precio = float(nuevo_precio)

    def __str__(self):
        return (f"{self.codigo} | {self.nombre} | ${self.precio:.2f} | "
                f"Existencias: {self.existencias} | Categoria: {self.categoria.nombre}")


class Cliente(Persistent):
    def __init__(self, id_cliente, nombre, telefono="", correo=""):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.ventas = PersistentList()

    def agregar_venta(self, id_venta):
        self.ventas.append(id_venta)

    def __str__(self):
        return f"{self.id_cliente} - {self.nombre}"


class DetalleVenta(Persistent):
    def __init__(self, producto, cantidad, precio_unitario):
        self.producto = producto
        self.cantidad = int(cantidad)
        self.precio_unitario = float(precio_unitario)

    def calcular_subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad} = ${self.calcular_subtotal():.2f}"


class Venta(Persistent):
    def __init__(self, id_venta, cliente):
        self.id_venta = id_venta
        self.fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.cliente = cliente
        self.detalles = PersistentList()
        self.finalizada = False

    def agregar_producto(self, producto, cantidad):
        if self.finalizada:
            print("La venta ya fue finalizada.")
            return False

        if producto.verificar_disponibilidad(cantidad):
            self.detalles.append(DetalleVenta(producto, cantidad, producto.precio))
            return True

        print("No hay suficientes existencias.")
        return False

    def calcular_total(self):
        return sum(detalle.calcular_subtotal() for detalle in self.detalles)

    def finalizar_venta(self):
        if self.finalizada or not self.detalles:
            return False

        for detalle in self.detalles:
            if not detalle.producto.verificar_disponibilidad(detalle.cantidad):
                return False

        for detalle in self.detalles:
            detalle.producto.disminuir_existencias(detalle.cantidad)

        self.finalizada = True
        self.cliente.agregar_venta(self.id_venta)
        return True

    def __str__(self):
        estado = "Finalizada" if self.finalizada else "Pendiente"
        return (f"{self.id_venta} | {self.fecha} | Cliente: {self.cliente.nombre} | "
                f"Total: ${self.calcular_total():.2f} | {estado}")


def abrir_bd():
    storage = FileStorage.FileStorage("tienda.fs")
    db = DB(storage)
    conexion = db.open()
    root = conexion.root()

    if "categorias" not in root:
        root.categorias = PersistentMapping()
    if "proveedores" not in root:
        root.proveedores = PersistentMapping()
    if "productos" not in root:
        root.productos = PersistentMapping()
    if "clientes" not in root:
        root.clientes = PersistentMapping()
    if "ventas" not in root:
        root.ventas = PersistentMapping()

    transaction.commit()
    return storage, db, conexion, root


def cerrar_bd(storage, db, conexion):
    transaction.commit()
    conexion.close()
    db.close()
    storage.close()


# -------------------------
# ALTAS
# -------------------------

def alta_categoria(root):
    id_categoria = input("ID de categoria: ")
    if id_categoria in root.categorias:
        print("La categoria ya existe.")
        return

    nombre = input("Nombre: ")
    descripcion = input("Descripcion: ")
    root.categorias[id_categoria] = Categoria(id_categoria, nombre, descripcion)
    transaction.commit()
    print("Categoria guardada.")


def alta_proveedor(root):
    id_proveedor = input("ID de proveedor: ")
    if id_proveedor in root.proveedores:
        print("El proveedor ya existe.")
        return

    nombre = input("Nombre: ")
    telefono = input("Telefono: ")
    correo = input("Correo: ")
    direccion = input("Direccion: ")

    root.proveedores[id_proveedor] = Proveedor(
        id_proveedor, nombre, telefono, correo, direccion
    )
    transaction.commit()
    print("Proveedor guardado.")


def alta_producto(root):
    codigo = input("Codigo del producto: ")
    if codigo in root.productos:
        print("El producto ya existe.")
        return

    nombre = input("Nombre: ")
    descripcion = input("Descripcion: ")

    try:
        precio = float(input("Precio: "))
        existencias = int(input("Existencias: "))
    except ValueError:
        print("Precio o existencias invalidos.")
        return

    print("Categorias disponibles:")
    for categoria in root.categorias.values():
        print(categoria)

    id_categoria = input("ID de categoria: ")
    if id_categoria not in root.categorias:
        print("La categoria no existe.")
        return

    root.productos[codigo] = Producto(
        codigo, nombre, descripcion, precio, existencias, root.categorias[id_categoria]
    )
    transaction.commit()
    print("Producto guardado.")


def alta_cliente(root):
    id_cliente = input("ID del cliente: ")
    if id_cliente in root.clientes:
        print("El cliente ya existe.")
        return

    nombre = input("Nombre: ")
    telefono = input("Telefono: ")
    correo = input("Correo: ")
    root.clientes[id_cliente] = Cliente(id_cliente, nombre, telefono, correo)
    transaction.commit()
    print("Cliente guardado.")


# -------------------------
# CONSULTAS
# -------------------------

def mostrar_productos(root):
    print("\n--- TODOS LOS PRODUCTOS ---")
    if not root.productos:
        print("No hay productos registrados.")
        return

    for producto in root.productos.values():
        print(producto)


def productos_precio_superior(root):
    try:
        limite = float(input("Precio minimo: $"))
    except ValueError:
        print("Cantidad invalida.")
        return

    encontrados = [p for p in root.productos.values() if p.precio > limite]
    print(f"\n--- PRODUCTOS CON PRECIO MAYOR A ${limite:.2f} ---")
    if not encontrados:
        print("No se encontraron productos.")
    else:
        for producto in encontrados:
            print(producto)


def productos_pocas_existencias(root):
    try:
        limite = int(input("Limite de existencias: "))
    except ValueError:
        print("Limite invalido.")
        return

    encontrados = [p for p in root.productos.values() if p.existencias < limite]
    print(f"\n--- PRODUCTOS CON EXISTENCIAS MENORES A {limite} ---")
    if not encontrados:
        print("No se encontraron productos.")
    else:
        for producto in encontrados:
            print(producto)


def productos_por_proveedor(root):
    id_proveedor = input("ID del proveedor: ")
    if id_proveedor not in root.proveedores:
        print("Proveedor no encontrado.")
        return

    proveedor = root.proveedores[id_proveedor]
    print(f"\n--- PRODUCTOS DE {proveedor.nombre} ---")
    if not proveedor.productos:
        print("Este proveedor no tiene productos asociados.")
        return

    for codigo in proveedor.productos:
        if codigo in root.productos:
            print(root.productos[codigo])


def total_ventas(root):
    total = sum(v.calcular_total() for v in root.ventas.values() if v.finalizada)
    print(f"\nTOTAL DE VENTAS: ${total:.2f}")


def reporte_venta_total_diaria(root):
    hoy = datetime.now().strftime("%d/%m/%Y")
    ventas_hoy = [
        v for v in root.ventas.values()
        if v.finalizada and v.fecha.startswith(hoy)
    ]

    total = sum(v.calcular_total() for v in ventas_hoy)

    print(f"\n--- REPORTE DE VENTA TOTAL DIARIA: {hoy} ---")
    if not ventas_hoy:
        print("No hay ventas registradas el dia de hoy.")
        print("TOTAL DEL DIA: $0.00")
        return

    for venta in ventas_hoy:
        print(venta)

    print(f"Ventas realizadas hoy: {len(ventas_hoy)}")
    print(f"TOTAL DEL DIA: ${total:.2f}")


def mostrar_ventas(root):
    print("\n--- VENTAS ---")
    if not root.ventas:
        print("No hay ventas registradas.")
        return

    for venta in root.ventas.values():
        print(venta)
        for detalle in venta.detalles:
            print("   ", detalle)


# -------------------------
# MODIFICACION Y ELIMINACION
# -------------------------

def modificar_producto(root):
    codigo = input("Codigo del producto: ")
    if codigo not in root.productos:
        print("Producto no encontrado.")
        return

    producto = root.productos[codigo]
    print("1. Cambiar precio")
    print("2. Incrementar existencias")
    opcion = input("Opcion: ")

    if opcion == "1":
        try:
            producto.actualizar_precio(float(input("Nuevo precio: ")))
            transaction.commit()
            print("Precio actualizado.")
        except ValueError:
            print("Precio invalido.")
    elif opcion == "2":
        try:
            producto.incrementar_existencias(int(input("Cantidad a agregar: ")))
            transaction.commit()
            print("Existencias actualizadas.")
        except ValueError:
            print("Cantidad invalida.")
    else:
        print("Opcion invalida.")


def asociar_producto_proveedor(root):
    id_proveedor = input("ID del proveedor: ")
    codigo = input("Codigo del producto: ")

    if id_proveedor not in root.proveedores:
        print("Proveedor no encontrado.")
        return
    if codigo not in root.productos:
        print("Producto no encontrado.")
        return

    root.proveedores[id_proveedor].agregar_producto(codigo)
    transaction.commit()
    print("Producto asociado al proveedor.")


def eliminar_producto(root):
    codigo = input("Codigo del producto a eliminar: ")
    if codigo not in root.productos:
        print("Producto no encontrado.")
        return

    for proveedor in root.proveedores.values():
        proveedor.quitar_producto(codigo)

    del root.productos[codigo]
    transaction.commit()
    print("Producto eliminado.")


# -------------------------
# LOGICA DE NEGOCIO
# -------------------------

def registrar_venta(root):
    id_venta = input("ID de la venta: ")
    if id_venta in root.ventas:
        print("La venta ya existe.")
        return

    id_cliente = input("ID del cliente: ")
    if id_cliente not in root.clientes:
        print("Cliente no encontrado.")
        return

    venta = Venta(id_venta, root.clientes[id_cliente])
    root.ventas[id_venta] = venta

    while True:
        codigo = input("Codigo del producto (0 para terminar): ")
        if codigo == "0":
            break
        if codigo not in root.productos:
            print("Producto no encontrado.")
            continue

        try:
            cantidad = int(input("Cantidad: "))
        except ValueError:
            print("Cantidad invalida.")
            continue

        if cantidad <= 0:
            print("La cantidad debe ser mayor a cero.")
            continue

        if venta.agregar_producto(root.productos[codigo], cantidad):
            print("Producto agregado a la venta.")

    if venta.finalizar_venta():
        transaction.commit()
        print(f"Venta registrada. Total: ${venta.calcular_total():.2f}")
        print("Inventario actualizado.")
    else:
        del root.ventas[id_venta]
        transaction.abort()
        print("No fue posible completar la venta.")


# -------------------------
# DATOS DE PRUEBA
# -------------------------

def cargar_datos_prueba(root):
    if root.productos:
        print("Ya existen datos. No se cargaron ejemplos.")
        return

    root.categorias["C01"] = Categoria("C01", "Abarrotes", "Productos de consumo")
    root.categorias["C02"] = Categoria("C02", "Bebidas", "Bebidas y refrescos")
    root.categorias["C03"] = Categoria("C03", "Limpieza", "Productos de limpieza")

    root.proveedores["PR01"] = Proveedor("PR01", "Distribuidora Xalapa", "2281111111", "ventas@distribuidora.com", "Xalapa")
    root.proveedores["PR02"] = Proveedor("PR02", "Proveedor del Centro", "2282222222", "contacto@centro.com", "Veracruz")

    root.productos["P001"] = Producto("P001", "Arroz", "Bolsa de arroz 1 kg", 28.50, 25, root.categorias["C01"])
    root.productos["P002"] = Producto("P002", "Refresco", "Refresco 600 ml", 20.00, 10, root.categorias["C02"])
    root.productos["P003"] = Producto("P003", "Detergente", "Detergente 1 kg", 45.00, 5, root.categorias["C03"])
    root.productos["P004"] = Producto("P004", "Cafe", "Cafe soluble", 75.00, 8, root.categorias["C01"])

    root.clientes["CL01"] = Cliente("CL01", "Juan Perez", "2283333333", "juan@email.com")
    root.clientes["CL02"] = Cliente("CL02", "Ana Lopez", "2284444444", "ana@email.com")

    root.proveedores["PR01"].agregar_producto("P001")
    root.proveedores["PR01"].agregar_producto("P002")
    root.proveedores["PR02"].agregar_producto("P003")
    root.proveedores["PR02"].agregar_producto("P004")

    transaction.commit()
    print("Datos de prueba guardados correctamente.")


# -------------------------
# MENU
# -------------------------

def menu(root):
    while True:
        print("\n==============================")
        print("     TIENDA LA ECONOMICA")
        print("==============================")
        print("1. Alta de producto")
        print("2. Alta de categoria")
        print("3. Alta de proveedor")
        print("4. Alta de cliente")
        print("5. Mostrar todos los productos")
        print("6. Modificar producto")
        print("7. Eliminar producto")
        print("8. Asociar producto a proveedor")
        print("9. Registrar venta")
        print("10. Productos por precio")
        print("11. Productos con pocas existencias")
        print("12. Productos por proveedor")
        print("13. Total de ventas")
        print("14. Reporte de venta total diaria")
        print("15. Mostrar ventas")
        print("16. Cargar datos de prueba")
        print("0. Salir")

        opcion = input("Selecciona una opcion: ")

        if opcion == "1":
            alta_producto(root)
        elif opcion == "2":
            alta_categoria(root)
        elif opcion == "3":
            alta_proveedor(root)
        elif opcion == "4":
            alta_cliente(root)
        elif opcion == "5":
            mostrar_productos(root)
        elif opcion == "6":
            modificar_producto(root)
        elif opcion == "7":
            eliminar_producto(root)
        elif opcion == "8":
            asociar_producto_proveedor(root)
        elif opcion == "9":
            registrar_venta(root)
        elif opcion == "10":
            productos_precio_superior(root)
        elif opcion == "11":
            productos_pocas_existencias(root)
        elif opcion == "12":
            productos_por_proveedor(root)
        elif opcion == "13":
            total_ventas(root)
        elif opcion == "14":
            reporte_venta_total_diaria(root)
        elif opcion == "15":
            mostrar_ventas(root)
        elif opcion == "16":
            cargar_datos_prueba(root)
        elif opcion == "0":
            print("Cerrando programa...")
            break
        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    storage, db, conexion, root = abrir_bd()

    print("\nBase de datos abierta.")
    print("Los datos guardados anteriormente siguen disponibles.")
    print(f"Productos almacenados: {len(root.productos)}")
    print(f"Clientes almacenados: {len(root.clientes)}")
    print(f"Ventas almacenadas: {len(root.ventas)}")

    try:
        menu(root)
    finally:
        cerrar_bd(storage, db, conexion)
        print("Base de datos cerrada correctamente.")
