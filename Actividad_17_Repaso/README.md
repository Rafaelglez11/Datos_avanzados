# Actividad 17 - Repaso BDOO

Proyecto de repaso de programación orientada a objetos y bases de datos orientadas a objetos utilizando Python y ZODB.

## Archivos

- `modelos.py`: contiene las clases `Recurso`, `Estudiante` y `Prestamo`.
- `base_datos.py`: abre e inicializa la base de datos ZODB.
- `main.py`: contiene el menú, registros, préstamos y las consultas.
- `RESPUESTAS.md`: contiene las respuestas de las preguntas de la actividad.
- `UML.md`: contiene el diagrama UML.
- `requirements.txt`: dependencias del proyecto.

## Instalación

Abrir una terminal dentro de la carpeta del proyecto.

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Después ejecutar:

```powershell
python main.py
```

La base de datos se creará automáticamente con el nombre:

`laboratorio.fs`

## Datos iniciales

El programa agrega cinco recursos:

1. NVIDIA RTX 4090
2. Jetson Orin
3. Robot móvil
4. Sensor LiDAR
5. Servidor IA

También agrega tres estudiantes:

- A001 - Ana López
- A002 - Carlos Pérez
- A003 - María Hernández

## Consultas implementadas

1. Todos los recursos.
2. Buscar recurso por identidad.
3. Recursos disponibles.
4. Recursos por tipo.
5. Recursos por fabricante.
6. Préstamos activos.
7. Navegación entre objetos.
8. Recursos GPU con costo mayor a $20,000.
9. Estadísticas de recursos.
10. Consulta propia usando dos clases, una relación y una condición.

## Persistencia

Los objetos se guardan dentro de `laboratorio.fs`.

Al cerrar y volver a ejecutar el programa, los objetos registrados continúan almacenados.
