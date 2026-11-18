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
- [ ] Se guardaron las capturas del código antes y después, el link al commit y el resultado de las pruebas.

## F. Resultado de la revisión

| Resultado | Cuándo corresponde |
| --- | --- |
| **Aprobada** | Se cumplen todos los criterios. |
| **Aprobada con observaciones** | Se cumplen todos los criterios de B y C, y hay observaciones menores en A, D o E que no afectan el comportamiento. Las observaciones se registran y se corrigen en un cambio posterior. |
| **Requiere correcciones** | Falla algún criterio de B o C. El Pull Request no se integra hasta corregirlo. |

## Resultado de cada revisión

| Pull Request | Autora | Revisora | Resultado |
| --- | --- | --- | --- |
| #1 Pruebas de caracterización | Emilce | Natalia | Aprobada |
| #2 Move Method | Emilce | Natalia | Aprobada |
| #3 Introduce Parameter Object | Emilce | Natalia | Aprobada con observaciones (búsqueda repetida del estudiante: queda como mejora futura) |
| #4 Extract Method | Natalia | Emilce | Aprobada con observaciones (import sin uso y línea con espacios: corregidos en el #5) |
| #5 Rename y Replace Magic Number with Constant | Natalia | Emilce | Aprobada (las observaciones menores sobre nombres y el salto de línea final se corrigieron antes de integrarlo) |
