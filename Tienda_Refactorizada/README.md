# Tienda La Económica

Proyecto en Python y ZODB refactorizado para separar responsabilidades.

## Estructura

- `modelos.py`: clases del sistema.
- `persistencia.py`: conexión, commit, abort y cierre de ZODB.
- `logica_negocio.py`: altas, modificaciones, inventario y ventas.
- `consultas.py`: consultas de productos y ventas.
- `main.py`: interfaz de línea de comandos.
- `requirements.txt`: dependencias.
- `.gitignore`: archivos que no deben subirse.

## Instalación

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecución

```powershell
python main.py
```

La base de datos se guarda en `tienda.fs`.

## Convenciones aplicadas

Se usan nombres descriptivos, constantes en mayúsculas, clases en PascalCase,
funciones y variables en snake_case, docstrings, validación de datos,
manejo de excepciones, separación de archivos y reducción de código duplicado.
