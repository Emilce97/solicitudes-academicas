# Decisiones técnicas

Este documento registra las decisiones más importantes que se tomaron durante el trabajo: qué se decidió, por qué y qué alternativas se descartaron.

## 1. Sistema base: un prototipo propio del caso sugerido

**Decisión.** Trabajar sobre un prototipo del Sistema de Gestión de Solicitudes Académicas, el caso sugerido por la cátedra, construido para este trabajo con asistencia de IA y con problemas de diseño incorporados de forma intencional.

**Por qué.** El equipo no contaba con un sistema previo adecuado, y la consigna admite "un prototipo construido por el equipo para este trabajo". Un sistema chico, de unas 360 líneas, permite concentrar el esfuerzo en el diagnóstico y la justificación, que es lo que se evalúa.

**Alternativas descartadas.** Un trabajo práctico anterior o un proyecto open source: ninguno garantizaba los problemas de diseño necesarios para aplicar los refactorings obligatorios.

**Consecuencia.** El uso de IA para generar la versión inicial se declara en el anexo A.1 del informe. Como los problemas eran conocidos de antemano, el diagnóstico no reproduce del todo la situación de un sistema real; esto se reconoce como límite del trabajo.

## 2. Python, consola y archivo JSON

**Decisión.** Python 3 con una interfaz de consola, sin librerías externas, y los datos guardados en `datos.json`, todos sintéticos.

**Por qué.** Es el lenguaje que el equipo maneja con más soltura, y la consola y el JSON evitan dependencias que no aportan al objetivo del trabajo. Se evaluó Java, que muestra los principios SOLID de forma más explícita, pero se priorizó que las dos integrantes pudieran explicar todo el código con seguridad.

## 3. Pruebas de caracterización antes de refactorizar

**Decisión.** Antes de modificar el código se escribieron 24 pruebas que registran el comportamiento de la versión inicial, y se ejecutaron después de cada refactoring.

**Por qué.** Un refactoring, por definición, no debe cambiar el comportamiento externo. Sin pruebas no había forma objetiva de demostrarlo.

**Cómo están hechas.**
- **Prueban a través del menú**, simulando lo que escribe la usuaria, y no los métodos internos. Así siguen siendo válidas aunque cambien los nombres o la estructura del código, que es justamente lo que hace un refactoring.
- **Trabajan sobre una copia temporal de los datos** (`tests/datos_prueba.json`), para no modificar nunca el `datos.json` real.
- **Fijan la fecha del día en el 16/11/2026**, porque el cálculo de vencimiento depende de la fecha de ejecución: sin fijarla, una prueba podría fallar con el paso del tiempo sin que cambie el código.

## 4. Orden de los refactorings

**Decisión.** Pruebas → Move Method → Extract Method e Introduce Parameter Object en paralelo → Rename y Replace Magic Number with Constant al final.

**Por qué.**
- El **Move Method** fue primero porque la regla de vencimiento también estaba copiada dentro de `reporte()`. Moverla antes a `Solicitud` permitió que el Extract Method la reutilizara, en lugar de extraer un método con la regla duplicada adentro.
- El **Extract Method** y el **Introduce Parameter Object** pudieron hacerse en paralelo porque modifican partes distintas del archivo.
- El **Rename** quedó al final porque cambia nombres en casi todas las líneas: hecho en paralelo, habría generado conflictos con todas las demás ramas.

## 5. Introduce Parameter Object con la clase `Estudiante`

**Decisión.** `crear_solicitud()` pasó de recibir ocho parámetros a recibir cuatro, usando como objeto parámetro la clase `Estudiante`, que ya existía.

**Por qué.** `Estudiante` agrupaba exactamente los cinco datos que viajaban sueltos. Crear una clase nueva con los mismos datos habría introducido duplicación.

**Observación de la revisión (PR #3).** `crear_solicitud()` vuelve a buscar al estudiante por legajo aunque el menú ya lo hizo. Se decidió mantener esa búsqueda para que el método no dependa de que quien lo llama haya verificado al estudiante. La causa de fondo es que el menú resuelve lógica propia de `Sistema`; queda como mejora futura (por ejemplo, un método `buscar_estudiante(legajo)` que usen los dos).

## 6. Regla de vencimiento con el mismo tratamiento en todo el sistema

**Decisión.** En el Extract Method, `reporte()` dejó de tener su propia copia de la regla y pasó a usar `esta_vencida()`. En el Rename se mantuvo la estructura `if/elif/else` del método.

**Por qué.** La regla original del reporte trataba de forma distinta una prioridad fuera del rango 1 a 3. Las dos versiones dan el mismo resultado para las prioridades válidas, que son las únicas que acepta el sistema; solo diferían si alguien escribía a mano una prioridad inválida en `datos.json`. Unificarlas eliminó la duplicación y, además, impide que el reporte y las búsquedas se contradigan. Conservar el `if/elif/else` evita cambiar ese tratamiento.

## 7. Alcance del Rename y de las constantes

**Decisión.** Se renombraron las variables poco descriptivas (`lst`, `resp`, `c1` a `c4`, entre otras) y se crearon constantes en `modelos.py` para las prioridades, los plazos de vencimiento, los estados y los tipos válidos. `id` pasó a `id_solicitud` e `id_responsable` para no tapar la función `id()` de Python.

**Qué no se cambió y por qué.**
- **Las variables de bucle de una letra** (`s`, `e`, `x`, `r`): son locales y de alcance corto, y cambiarlas aumentaba el riesgo sin un beneficio claro.
- **Los textos que ve el usuario** (las etiquetas "Alta", "Media" y "Baja", el ancho del reporte y los textos del menú): cambiarlos habría alterado el comportamiento externo.
- **El parámetro `id` de los constructores de `Responsable` y `Solicitud`** en `modelos.py`: mismo criterio, es un nombre local de alcance corto (PR #5).
- **La estructura `if/elif/else` de `esta_vencida()`**: agregar una prioridad nueva todavía obliga a modificar ese método, por lo que el principio abierto/cerrado (OCP) quedó cumplido solo en parte. Se resolvería con un diccionario de plazos y una tabla de transiciones (informe, sección 6.1).


## 8. Lo que quedó fuera del alcance

**Decisión.** No se corrigieron el manejo de errores, el alto acoplamiento ni la concentración de responsabilidades en la clase `Sistema`, aunque se diagnosticaron.

**Por qué.**
- **El manejo de errores**, a pesar de tener prioridad alta, no se resuelve con un refactoring: corregirlo cambia lo que hace el sistema (por ejemplo, mostrar un mensaje en lugar de detenerse ante una entrada inválida). Debe abordarse como una corrección, con sus propias pruebas. Es la primera mejora futura propuesta.
- **El acoplamiento y la separación de `Sistema` en componentes** (modelo, lógica, persistencia e interfaz) requieren reestructurar gran parte del código, con un esfuerzo que excede este trabajo. Los refactorings aplicados avanzan en esa dirección.

Las mejoras pendientes y su orden están en la sección 10.3 del informe.

## 9. Flujo de trabajo en Git

**Decisión.**
- Una rama por cambio, con el formato `autora/técnica`.
- Integración a `main` solo mediante Pull Requests revisados por la otra integrante.
- Unión con *Create a merge commit*, no con *Squash and merge*.

**Por qué.** La revisión cruzada deja registrada en el repositorio la conversación de cada cambio. El *merge commit* conserva cada commit con su autora, que es la evidencia de quién hizo qué, y evita que una rama creada a partir de otra muestre cambios repetidos en su Pull Request.

**Ramas dependientes.** Las ramas del Move Method y del Introduce Parameter Object se crearon a partir de la rama de las pruebas, que todavía no estaba integrada, para poder verificar cada cambio. Sus Pull Requests se abrieron recién cuando las pruebas estuvieron en `main`.

## 10. Criterio para aprobar con observaciones

**Decisión.** Un Pull Request se aprueba si cumple todos los criterios de comportamiento y alcance del checklist. Las observaciones menores de prolijidad o diseño se registran y se corrigen en un cambio posterior.

**Por qué.** Mantiene cada Pull Request acotado a un solo cambio y facilita su revisión, sin dejar de registrar lo que hay que mejorar. Por ejemplo, el import sin uso y la línea con espacios observados en el PR #4 se corrigieron en el PR #5.

## 11. Verificación doble: pruebas y comparación de salidas

**Decisión.** Además de las 24 pruebas automáticas, en cada refactoring se ejecutó el sistema con las mismas entradas antes y después, y se comparó lo que imprime con `diff`.

**Por qué.** Las pruebas verifican las reglas, pero la comparación de salidas detecta cambios en el formato exacto de lo que se muestra y cubre casos que las pruebas no tienen, como los plazos de 10 y 20 días. Se hizo el mismo día, porque el reporte y el vencimiento dependen de la fecha. Los resultados están en [`evidencias.md`](evidencias.md).

## 12. Versionado: tags

**Decisión.** Marcar con tags los estados generales (`estado-inicial` y `estado-refactorizado`) y el hito de cada etapa (`etapa-diagnostico`, `etapa-pruebas`, `etapa-refactoring` y `etapa-docs`).

**Por qué.** Permite ver y comparar la versión base y la versión final del código, y ubicar en el historial dónde terminó cada etapa. La lista de tags y lo que marca cada uno está en [`evidencias.md`](evidencias.md).