# Checklist de code review

Cada Pull Request fue revisado por la integrante que no lo había escrito, siguiendo esta lista de criterios. Redacción: Natalia Córdoba. Ajustes: Emilce Spital.

## A. Proceso

- [ ] La rama sale de `main` y su nombre sigue el formato `autora/técnica`. Si depende de un cambio todavía no integrado, sale de esa rama y su Pull Request se abre recién cuando ese cambio está en `main`.
- [ ] Los commits tienen la identidad de la autora (`git log --format="%an %s"`).
- [ ] Cada commit corresponde a un paso lógico y su mensaje lo explica.
- [ ] La descripción del Pull Request indica el smell que resuelve y cómo se verificó.

## B. Comportamiento

- [ ] Todas las pruebas pasan (`python -m unittest discover -s tests -v`).
- [ ] Las pruebas no se modificaron para que pasen, o el cambio está justificado (`git diff main...rama -- tests/`).
- [ ] La salida del sistema es idéntica antes y después (comparación de salidas con los mismos comandos, el mismo día).
- [ ] `datos.json` no quedó modificado por las pruebas (`git status`).

## C. Alcance

- [ ] El cambio resuelve el smell declarado en el informe (no aplica al Pull Request de las pruebas).
- [ ] No agrega funcionalidad ni corrige errores a escondidas.
- [ ] No toca los smells asignados a la otra integrante.

## D. Calidad del código

- [ ] Los nombres nuevos dicen qué contienen.
- [ ] No hay imports, variables ni código sin uso.
- [ ] No hay duplicación ni números o textos mágicos nuevos.
- [ ] No hay espacios sobrantes (`git diff --check`).

## E. Diseño y evidencia

- [ ] El cambio mejora una responsabilidad, el acoplamiento o la cohesión, y se puede decir en una frase cuál.
- [ ] Se guardaron las capturas del código antes y después (en el informe, secciones 7 y 8.2), el link al commit y el resultado de las pruebas.

## F. Resultado de la revisión

| Resultado | Cuándo corresponde |
| --- | --- |
| **Aprobada** | Se cumplen todos los criterios. |
| **Aprobada con observaciones** | Se cumplen todos los criterios de B y C, y hay observaciones menores en A, D o E que no afectan el comportamiento. Las observaciones se registran y se corrigen en un cambio posterior, aunque también se admite corregirlas dentro del mismo PR antes del merge. |
| **Requiere correcciones** | Falla algún criterio de B o C. El Pull Request no se integra hasta corregirlo. |

## Resultado de cada revisión

| Pull Request | Autora | Revisora | Qué se verificó | Resultado |
| --- | --- | --- | --- | --- |
| [#1 Pruebas de caracterización](https://github.com/Emilce97/solicitudes-academicas/pull/1) | Emilce | Natalia | 24 pruebas OK; no modifica `sistema.py`, `modelos.py` ni `main.py` (línea base confiable); usan `tests/datos_prueba.json` sin tocar `datos.json`; fijan la fecha, así que no dependen del día; cubren registrar, asignar, cambiar estado, búsquedas, reporte y vencimiento, incluida la prioridad fuera de rango; cambio en `.gitignore` correcto | Aprobada |
| [#2 Move Method](https://github.com/Emilce97/solicitudes-academicas/pull/2) | Emilce | Natalia | 24 pruebas OK; `tests/` sin cambios; salida de las búsquedas idéntica en `main` y en la rama | Aprobada |
| [#3 Introduce Parameter Object](https://github.com/Emilce97/solicitudes-academicas/pull/3) | Emilce | Natalia | 24 OK; validación del tipo antes del alta; salida idéntica (estudiante nuevo, existente y búsqueda) | Aprobada con observaciones |
| [#4 Extract Method](https://github.com/Emilce97/solicitudes-academicas/pull/4) | Natalia | Emilce | 24 OK; salida idéntica de búsquedas y reporte | Aprobada con observaciones |
| [#5 Rename y constantes](https://github.com/Emilce97/solicitudes-academicas/pull/5) | Natalia | Emilce | 24 OK; `git diff --check` limpio; recorrido completo del menú idéntico (234 líneas); plazos probados en 92 fechas (1/10 al 31/12) | Aprobada con observaciones (corregidas antes de integrar) |

## Observaciones y acciones correctivas

| Observación | PR | Acción | Dónde quedó |
| --- | --- | --- | --- |
| `crear_solicitud()` vuelve a buscar al estudiante aunque el menú ya lo hizo | #3 | No bloqueante; mejora futura: `buscar_estudiante(legajo)` | Decisiones técnicas, punto 5 |
| `datetime` quedó importado sin uso | #4 | Corregido | PR #5 |
| Línea en blanco con espacios antes de `def reporte` | #4 | Corregido | PR #5 |
| Nombres cortos que no son de bucle (`res`, `est`, `nuevo`) | #5 | Renombrados a `resultados`, `estudiante`/`estudiante_encontrado`, `nuevo_estado` | Commit `e33a1f5` |
| Falta el salto de línea final en `modelos.py` | #5 | Agregado | Mismo commit |
