# Actividad 16 - Base de datos orientada a objetos con ZODB

Proyecto de biblioteca realizado con Python y ZODB.

## Archivos

- `01_objetos.py`: objetos, estado, propiedades y comportamiento.
- `02_identidad.py`: identidad de objetos.
- `03_propiedades.py`: propiedades de la clase Libro.
- `04_comportamiento.py`: préstamo y devolución de libros.
- `05_persistencia.py`: conexión y persistencia con ZODB.
- `06_diseno_bdoo.py`: autores, libros, usuarios, préstamos y relaciones.
- `07_consultas.py`: consultas sobre los libros almacenados.

## Instalación

```bash
pip install ZODB
```

## Orden recomendado de ejecución

```bash
python 01_objetos.py
python 02_identidad.py
python 03_propiedades.py
python 04_comportamiento.py
python 05_persistencia.py
python 06_diseno_bdoo.py
python 07_consultas.py
```

Para las consultas de `07_consultas.py`, se debe ejecutar primero `06_diseno_bdoo.py` para cargar los datos en `biblioteca.fs`.
