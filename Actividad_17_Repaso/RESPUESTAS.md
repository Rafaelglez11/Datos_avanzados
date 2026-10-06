# Respuestas de la Actividad 17

## Parte I

### ¿Qué diferencia existe entre la clase Recurso y los objetos recurso1, recurso2, etc.?

La clase `Recurso` es como una plantilla que define qué datos y funciones tendrán los recursos. En cambio, `recurso1`, `recurso2` y los demás son objetos creados a partir de esa clase y cada uno contiene sus propios valores.

---

## Parte II

### ¿Por qué la identidad de un objeto no debería depender únicamente de su nombre?

Porque pueden existir dos recursos con el mismo nombre. Por eso se utiliza un identificador único como `id_recurso`, ya que permite distinguir cada objeto aunque tengan datos parecidos.

---

## Parte III

### Diferencia entre identidad y propiedades

La identidad es el dato que permite reconocer un objeto de manera única. En este caso se utiliza `id_recurso`.

Las propiedades son las características del objeto, por ejemplo su nombre, tipo, costo, marca, modelo y disponibilidad.

---

## Parte IV

### Diferencia entre recurso1.disponible y recurso1.esta_disponible()

`recurso1.disponible` accede directamente al atributo que guarda el estado del recurso.

`recurso1.esta_disponible()` ejecuta un método de la clase que devuelve el valor de ese atributo.

La segunda forma permite controlar mejor la manera en que se consulta la información del objeto.

---

## Parte VII

### ¿Qué significa prestamo.recurso.marca?

Primero se accede al objeto `prestamo`.

Después se accede al objeto `recurso` que está relacionado con ese préstamo.

Finalmente se obtiene el atributo `marca` del recurso.

El recorrido es:

`Prestamo -> Recurso -> marca`

---

## Parte XII

### Diferencia entre recurso = Recurso(...) y root.recursos[recurso.id_recurso] = recurso

`recurso = Recurso(...)` solamente crea el objeto en memoria mientras el programa se está ejecutando.

`root.recursos[recurso.id_recurso] = recurso` guarda una referencia al objeto dentro de la estructura persistente de ZODB.

Después de ejecutar `transaction.commit()`, el objeto queda almacenado en la base de datos y puede seguir existiendo aunque el programa se cierre.

---

## Consulta 10

### Consulta propuesta

La consulta muestra los préstamos activos de estudiantes de Ingeniería en IA que tengan prestado un recurso de la marca NVIDIA.

Esta consulta utiliza las clases:

- `Prestamo`
- `Estudiante`
- `Recurso`

La relación se realiza porque un préstamo contiene una referencia al estudiante y otra al recurso.

La condición utilizada es que el préstamo esté activo, el estudiante pertenezca a Ingeniería en IA y el recurso sea de la marca NVIDIA.

### Problema que resuelve

Permite saber qué estudiantes de Ingeniería en IA tienen actualmente prestado algún equipo NVIDIA del laboratorio.
