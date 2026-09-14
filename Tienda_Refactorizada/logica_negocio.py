"""Lógica de negocio."""
from datetime import datetime
from modelos import Categoria, Cliente, DetalleVenta, Producto, Proveedor, Venta
from persistencia import guardar_cambios, cancelar_cambios

def validar_texto(valor, campo):
    """Valida texto obligatorio."""
    valor = str(valor).strip()
    if not valor:
        raise ValueError(f"{campo} no puede estar vacío.")
    return valor

def registrar_categoria(raiz, id_categoria, nombre, descripcion=""):
    """Registra una categoría."""
    id_categoria = validar_texto(id_categoria, "ID categoría")
    if id_categoria in raiz.categorias:
        raise ValueError("La categoría ya existe.")
    categoria = Categoria(id_categoria, validar_texto(nombre, "Nombre"), descripcion)
    raiz.categorias[id_categoria] = categoria
    guardar_cambios()
    return categoria

def registrar_proveedor(raiz, id_proveedor, nombre, telefono="", correo="", direccion=""):
    """Registra un proveedor."""
    id_proveedor = validar_texto(id_proveedor, "ID proveedor")
    if id_proveedor in raiz.proveedores:
        raise ValueError("El proveedor ya existe.")
    proveedor = Proveedor(id_proveedor, validar_texto(nombre, "Nombre"), telefono, correo, direccion)
    raiz.proveedores[id_proveedor] = proveedor
    guardar_cambios()
    return proveedor

def registrar_cliente(raiz, id_cliente, nombre, telefono="", correo=""):
    """Registra un cliente."""
    id_cliente = validar_texto(id_cliente, "ID cliente")
    if id_cliente in raiz.clientes:
        raise ValueError("El cliente ya existe.")
    cliente = Cliente(id_cliente, validar_texto(nombre, "Nombre"), telefono, correo)
    raiz.clientes[id_cliente] = cliente
    guardar_cambios()
    return cliente

def registrar_producto(raiz, codigo, nombre, descripcion, precio, existencias, id_categoria):
    """Registra un producto."""
    codigo = validar_texto(codigo, "Código")
    if codigo in raiz.productos:
        raise ValueError("El producto ya existe.")
    if id_categoria not in raiz.categorias:
        raise ValueError("La categoría no existe.")
    precio = float(precio)
    existencias = int(existencias)
    if precio <= 0 or existencias < 0:
        raise ValueError("Precio o existencias inválidos.")
    producto = Producto(codigo, validar_texto(nombre, "Nombre"), descripcion, precio, existencias, raiz.categorias[id_categoria])
    raiz.productos[codigo] = producto
    guardar_cambios()
    return producto

def obtener_producto(raiz, codigo):
    """Obtiene un producto por código."""
    if codigo not in raiz.productos:
        raise ValueError("Producto no encontrado.")
    return raiz.productos[codigo]

def modificar_precio_producto(raiz, codigo, precio):
    """Modifica el precio de un producto."""
    producto = obtener_producto(raiz, codigo)
    producto.actualizar_precio(precio)
    guardar_cambios()
    return producto

def incrementar_inventario(raiz, codigo, cantidad):
    """Incrementa el inventario."""
    cantidad = int(cantidad)
    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor a cero.")
    producto = obtener_producto(raiz, codigo)
    producto.incrementar_existencias(cantidad)
    guardar_cambios()
    return producto

def eliminar_producto(raiz, codigo):
    """Elimina un producto."""
    producto = obtener_producto(raiz, codigo)
    for proveedor in raiz.proveedores.values():
        proveedor.quitar_producto(codigo)
    del raiz.productos[codigo]
    guardar_cambios()
    return producto

def asociar_producto_proveedor(raiz, id_proveedor, codigo):
    """Asocia producto y proveedor."""
    if id_proveedor not in raiz.proveedores:
        raise ValueError("Proveedor no encontrado.")
    obtener_producto(raiz, codigo)
    raiz.proveedores[id_proveedor].agregar_producto(codigo)
    guardar_cambios()

def registrar_venta(raiz, id_venta, id_cliente, productos):
    """Registra una venta y actualiza inventario."""
    if id_venta in raiz.ventas:
        raise ValueError("La venta ya existe.")
    if id_cliente not in raiz.clientes:
        raise ValueError("Cliente no encontrado.")
    if not productos:
        raise ValueError("La venta debe tener productos.")
    cliente = raiz.clientes[id_cliente]
    venta = Venta(id_venta, cliente, datetime.now().strftime("%d/%m/%Y %H:%M"))
    try:
        for codigo, cantidad in productos:
            producto = obtener_producto(raiz, codigo)
            cantidad = int(cantidad)
            if cantidad <= 0 or not producto.verificar_disponibilidad(cantidad):
                raise ValueError(f"Cantidad inválida o stock insuficiente para {producto.nombre}.")
            venta.agregar_detalle(DetalleVenta(producto, cantidad, producto.precio))
        for detalle in venta.detalles:
            detalle.producto.disminuir_existencias(detalle.cantidad)
        venta.finalizada = True
        cliente.agregar_venta(id_venta)
        raiz.ventas[id_venta] = venta
        guardar_cambios()
        return venta
    except Exception:
        cancelar_cambios()
        raise
