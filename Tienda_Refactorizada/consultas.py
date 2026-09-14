"""Consultas del sistema."""
from collections import Counter
from datetime import datetime

def todos_los_productos(raiz):
    """Devuelve todos los productos."""
    return list(raiz.productos.values())

def productos_disponibles(raiz):
    """Devuelve productos con existencias."""
    return [p for p in raiz.productos.values() if p.existencias > 0]

def productos_bajo_stock(raiz, limite):
    """Devuelve productos con poco inventario."""
    return [p for p in raiz.productos.values() if p.existencias < int(limite)]

def productos_por_proveedor(raiz, id_proveedor):
    """Devuelve productos de un proveedor."""
    if id_proveedor not in raiz.proveedores:
        raise ValueError("Proveedor no encontrado.")
    proveedor = raiz.proveedores[id_proveedor]
    return [raiz.productos[c] for c in proveedor.productos if c in raiz.productos]

def ventas_cliente(raiz, id_cliente):
    """Devuelve las ventas de un cliente."""
    if id_cliente not in raiz.clientes:
        raise ValueError("Cliente no encontrado.")
    cliente = raiz.clientes[id_cliente]
    return [raiz.ventas[v] for v in cliente.ventas if v in raiz.ventas]

def total_ventas(raiz):
    """Calcula el total histórico de ventas."""
    return sum(v.calcular_total() for v in raiz.ventas.values() if v.finalizada)

def venta_total_diaria(raiz, fecha=None):
    """Genera el reporte de venta total diaria."""
    fecha = fecha or datetime.now().strftime("%d/%m/%Y")
    ventas = [v for v in raiz.ventas.values() if v.finalizada and v.fecha.startswith(fecha)]
    return {"fecha": fecha, "cantidad_ventas": len(ventas), "ventas": ventas,
            "total": sum(v.calcular_total() for v in ventas)}

def productos_mas_vendidos(raiz):
    """Devuelve productos ordenados por unidades vendidas."""
    contador = Counter()
    for venta in raiz.ventas.values():
        if venta.finalizada:
            for detalle in venta.detalles:
                contador[detalle.producto.codigo] += detalle.cantidad
    return [(raiz.productos[c], n) for c, n in contador.most_common() if c in raiz.productos]
