"""Modelos del sistema."""
from persistent import Persistent
from persistent.list import PersistentList

class Categoria(Persistent):
    """Representa una categoría."""
    def __init__(self, id_categoria, nombre, descripcion=""):
        self.id_categoria = id_categoria
        self.nombre = nombre
        self.descripcion = descripcion
    def __str__(self):
        return f"{self.id_categoria} - {self.nombre}"

class Proveedor(Persistent):
    """Representa un proveedor."""
    def __init__(self, id_proveedor, nombre, telefono="", correo="", direccion=""):
        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion
        self.productos = PersistentList()
    def agregar_producto(self, codigo):
        if codigo not in self.productos:
            self.productos.append(codigo)
    def quitar_producto(self, codigo):
        if codigo in self.productos:
            self.productos.remove(codigo)

class Producto(Persistent):
    """Representa un producto."""
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
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")
        if cantidad > self.existencias:
            raise ValueError("No hay existencias suficientes.")
        self.existencias -= cantidad
    def verificar_disponibilidad(self, cantidad=1):
        return self.existencias >= int(cantidad)
    def actualizar_precio(self, precio):
        precio = float(precio)
        if precio <= 0:
            raise ValueError("El precio debe ser mayor a cero.")
        self.precio = precio
    def __str__(self):
        return f"{self.codigo} | {self.nombre} | ${self.precio:.2f} | Existencias: {self.existencias}"

class Cliente(Persistent):
    """Representa un cliente."""
    def __init__(self, id_cliente, nombre, telefono="", correo=""):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.ventas = PersistentList()
    def agregar_venta(self, id_venta):
        if id_venta not in self.ventas:
            self.ventas.append(id_venta)

class DetalleVenta(Persistent):
    """Representa un producto dentro de una venta."""
    def __init__(self, producto, cantidad, precio_unitario):
        self.producto = producto
        self.cantidad = int(cantidad)
        self.precio_unitario = float(precio_unitario)
    def calcular_subtotal(self):
        return self.cantidad * self.precio_unitario

class Venta(Persistent):
    """Representa una venta."""
    def __init__(self, id_venta, cliente, fecha):
        self.id_venta = id_venta
        self.cliente = cliente
        self.fecha = fecha
        self.detalles = PersistentList()
        self.finalizada = False
    def agregar_detalle(self, detalle):
        self.detalles.append(detalle)
    def calcular_total(self):
        return sum(d.calcular_subtotal() for d in self.detalles)
