# Sistema de Gestión de Solicitudes Académicas

> Repositorio del Trabajo Práctico Integrador (TPI) de Metodología de Sistemas II  
> **Carrera:** Tecnicatura Universitaria en Programación a Distancia (UTN)  
> **Docentes:** Aristiaran, Martín León - Videla, Flavia  
> **Tutores:** Londero, Guillermo Humberto - Naveda, Claudia  
> **Integrantes:**
> - Córdoba Natalia - Comisión N° 7
> - Spital Emilce - Comisión N° 9

## Entrega final

| Recurso | Enlace |
| :--- | :--- |
| Video explicativo | https://www.youtube.com/watch?v=_y3VTFhkgIg |

## Descripción

Prototipo de consola en Python para registrar y seguir solicitudes de estudiantes
(certificados, cambios de comisión, reclamos de nota y otros trámites).
Se usa como caso de estudio del TPI: diagnóstico de calidad, deuda técnica,
refactoring y revisión técnica de un sistema existente.

Todos los datos de `datos.json` son sintéticos.

## Funcionalidades

- Registrar una solicitud (da de alta al estudiante si no existe).
- Asignar un responsable.
- Cambiar el estado (PENDIENTE, EN_PROCESO, RESUELTA, RECHAZADA) con transiciones válidas.
- Buscar por estado, por tipo o por legajo del estudiante, marcando las vencidas.
- Generar un reporte (por estado, tipo y prioridad, vencidas y carga por responsable).
- Listar responsables.

## Requisitos e instalación

- Python 3. No usa librerías externas.

```bash
git clone https://github.com/Emilce97/solicitudes-academicas.git
cd solicitudes-academicas
```

## Uso

Desde la carpeta del proyecto:

```bash
python main.py
```

El sistema lee y guarda sus datos en `datos.json`, por lo que debe ejecutarse desde esa carpeta.

## Pruebas

```bash
python -m unittest discover -s tests -v
```

Son 24 pruebas de caracterización que fijan el comportamiento del sistema; deben dar OK
antes y después de cada refactoring. Usan una copia temporal de los datos y una fecha fija,
así que no modifican `datos.json` y su resultado no depende del día en que se ejecutan.

## Estructura

| Archivo/Carpeta | Qué hace |
| --- | --- |
| `main.py` | Punto de entrada |
| `modelos.py` | Entidades (Estudiante, Responsable, Solicitud) y constantes del dominio. |
| `sistema.py` | Lógica del sistema, persistencia, reporte y menú |
| `datos.json` | Datos sintéticos |
| `tests/` | Pruebas de caracterización |
| `docs/` | Checklist de code review, evidencias y decisiones técnicas |

## Versiones y flujo de trabajo

- **Tag `estado-inicial`:** versión base con los problemas de diseño a diagnosticar.
- **Tag `estado-refactorizado`:** estado final tras los refactorings.
- **Trabajo en ramas:** cada cambio se hizo en una rama propia (`emilce/...`, `natalia/...`)
  y se integró a `main` mediante un pull request revisado por la otra integrante.
- **Tags de etapa:** `etapa-diagnostico`, `etapa-pruebas`, `etapa-refactoring` y `etapa-docs`
  marcan el commit donde terminó cada etapa (detalle en `docs/evidencias.md`(docs/evidencias.md)).

## Refactorings aplicados

| Refactoring | Rama | Pull request | Autora |
| --- | --- | --- | --- |
| Move Method | `emilce/move-method` | [#2](https://github.com/Emilce97/solicitudes-academicas/pull/2) | Emilce |
| Introduce Parameter Object | `emilce/parameter-object` | [#3](https://github.com/Emilce97/solicitudes-academicas/pull/3) | Emilce |
| Extract Method | `natalia/extract-method` | [#4](https://github.com/Emilce97/solicitudes-academicas/pull/4) | Natalia |
| Rename y Replace Magic Number with Constant | `natalia/rename` | [#5](https://github.com/Emilce97/solicitudes-academicas/pull/5) | Natalia |

## Tecnologías

Python 3 (módulos estándar `json` y `datetime`), `unittest`, Git y GitHub.
