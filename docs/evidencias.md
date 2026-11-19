# Evidencias

Este documento indica dónde está cada evidencia del trabajo y cómo reproducir la verificación. Las capturas de pantalla están en el informe PDF; acá se resumen en texto.

## Dónde está cada evidencia

| Etapa | Evidencia en el repositorio | Informe |
| --- | --- | --- |
| Sistema base | Tag `estado-inicial` | 2.4 |
| Pruebas | `tests/test_caracterizacion.py` (24 casos), PR #1, tag `etapa-pruebas` | 8 |
| Refactorings | Pull Requests #2 a #5, tag `etapa-refactoring` | 7 |
| Verificación antes/después | Secciones de este documento | 8.2 |
| Code review | [`checklist-code-review.md`](checklist-code-review.md) y las conversaciones de cada Pull Request | 9 |
| Decisiones técnicas | [`decisiones-tecnicas.md`](decisiones-tecnicas.md) | 4.3 y 10 |
| Documentación | Pull Request #6, tag `etapa-docs` | Anexo A.3 |
| Estado final | Tag `estado-refactorizado` | 7 |

Otros recursos:

- **Pull Requests #1 a #6** de este repositorio: revisión de cada cambio, con los comentarios y las verificaciones realizadas.
- **Informe del TPI:** capturas del funcionamiento (sección 2.4), de la ejecución de las pruebas antes y después de cada refactoring (sección 8.2) y de las revisiones de código (sección 9.2).
- **ZIP de la entrega:** contiene el informe en PDF (`informe/`), el código de la versión inicial (`codigo/estado-inicial/`) y el código final con pruebas, README y `/docs` (`codigo/estado-refactorizado/`).
- **Pruebas automáticas:** `tests/test_caracterizacion.py` (24 casos). Se ejecutan con `python -m unittest discover -s tests -v`.

## Resultado de las pruebas (informe, sección 8.2)

Las 24 pruebas de caracterización se ejecutaron sobre la versión inicial y después de cada refactoring, sin modificar las pruebas.

| Momento | Versión del código | Resultado |
| --- | --- | --- |
| Antes | Versión inicial (`estado-inicial`) | 24 de 24 OK |
| Después del refactoring 1 | Move Method | 24 de 24 OK |
| Después del refactoring 2 | Introduce Parameter Object | 24 de 24 OK |
| Después del refactoring 3 | Extract Method | 24 de 24 OK |
| Después del refactoring 4 | Rename y constantes | 24 de 24 OK |

## Comparación de salidas antes y después

Además de las pruebas automáticas, se ejecutó el sistema con las mismas entradas antes y después de cada cambio y se comparó lo que imprime. Se hizo el mismo día, porque el reporte y el vencimiento dependen de la fecha.

**Extract Method.** Búsqueda por estado, por tipo y por estudiante, y reporte (la salida tiene 115 líneas):

```
$ printf '4\nPENDIENTE\n4\nRESUELTA\n5\nCERTIFICADO\n6\n10001\n7\n0\n' | python main.py > antes_extract.txt
(se aplica el refactoring)
$ printf '4\nPENDIENTE\n4\nRESUELTA\n5\nCERTIFICADO\n6\n10001\n7\n0\n' | python main.py > despues_extract.txt
$ diff antes_extract.txt despues_extract.txt && echo "salidas idénticas"
salidas idénticas
```

**Rename y constantes.** Recorrido completo del menú (altas, asignación, cambios de estado válidos e inválidos, errores, búsquedas, reporte y listado de responsables), con una salida de 234 líneas, idéntica en `main` y en la rama:

```
$ diff antes_rename.txt despues_rename.txt && echo "salidas idénticas"
salidas idénticas
$ diff plazos_antes.txt plazos_despues.txt && echo "plazos idénticos"
plazos idénticos
```

Resultado del chequeo de plazos de vencimiento, igual antes y después:

```
prioridad 1 - dias 5  - vencida: False
prioridad 1 - dias 6  - vencida: True
prioridad 2 - dias 10 - vencida: False
prioridad 2 - dias 11 - vencida: True
prioridad 3 - dias 20 - vencida: False
prioridad 3 - dias 21 - vencida: True
```

Los plazos de 10 y 20 días no tienen prueba automática. En la revisión del Pull Request #5 se verificaron además comparando un recorrido completo del menú para cada día del 1/10 al 31/12 (92 fechas): la salida fue idéntica.

**Move Method e Introduce Parameter Object.** Se comparó manualmente la salida del menú en `main` y en la rama del cambio, con los mismos comandos (alta con estudiante nuevo y existente, búsquedas). En ambos casos fue idéntica.

## Cómo reproducir la verificación

```
git clone https://github.com/Emilce97/solicitudes-academicas.git
cd solicitudes-academicas
python -m unittest discover -s tests -v    # 24 pruebas, deben dar OK
python main.py                             # menú; la opción 7 muestra el reporte
```

Las pruebas usan una copia temporal de `tests/datos_prueba.json` y fijan la fecha en el 16/11/2026, por lo que no modifican `datos.json` y dan el mismo resultado cualquier día. En cambio, si se usa el menú para registrar o modificar solicitudes, `datos.json` sí cambia; para volver a los datos originales: `git restore datos.json`.

## Límites de la verificación

Las pruebas registran el comportamiento actual, incluidos sus defectos: no cubren el ingreso de letras donde se espera un número ni un `datos.json` dañado, porque esos problemas no se corrigieron en este trabajo (informe, secciones 8.3 y 10.3).

## Participación de cada integrante

El reparto de tareas está en el anexo A.5 del informe. 

## Tags del repositorio

| Tag | Qué marca |
| --- | --- |
| `estado-inicial` | Versión base con los problemas de diseño a diagnosticar |
| `etapa-diagnostico` | Diagnóstico de la versión base |
| `etapa-pruebas` | Pruebas de caracterización integradas a `main` |
| `etapa-refactoring` | Los cuatro refactorings integrados a `main` |
| `etapa-docs` | README y carpeta `/docs` |
| `estado-refactorizado` | Estado final del código |