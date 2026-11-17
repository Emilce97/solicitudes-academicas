"""
Pruebas de caracterización del Sistema de Gestión de Solicitudes Académicas.

Registran cómo se comporta HOY la versión inicial (tag estado-inicial), vista
desde afuera: lo que la usuaria escribe en el menú, lo que ve en pantalla y lo
que queda guardado en el archivo de datos. Después de cada refactoring se
vuelven a correr: si todas pasan, el comportamiento externo no cambió.

Cómo correrlas, desde la carpeta del proyecto:
    python -m unittest discover -s tests -v

Detalles importantes:
- Usan una copia de tests/datos_prueba.json en una carpeta temporal, así
  nunca modifican el datos.json real.
- Fijan la fecha de "hoy" en el 16/11/2026, porque el cálculo de vencimiento
  depende del día en que se ejecuta el programa.
"""

import io
import json
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import date
from unittest import mock

import sistema

CARPETA_TESTS = os.path.dirname(os.path.abspath(__file__))
DATOS_PRUEBA = os.path.join(CARPETA_TESTS, "datos_prueba.json")
HOY = date(2026, 11, 16)


def fecha_fija(dia):
    """Crea una versión de `date` cuyo today() devuelve siempre el día indicado."""

    class FechaFija(date):
        @classmethod
        def today(cls):
            return dia

    return FechaFija


class PruebaBase(unittest.TestCase):
    """Prepara un archivo de datos temporal y fija la fecha de hoy."""

    hoy = HOY

    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.ruta_datos = os.path.join(carpeta.name, "datos.json")
        shutil.copy(DATOS_PRUEBA, self.ruta_datos)

        # El sistema lee y escribe el archivo indicado en ARCHIVO:
        # lo apuntamos a la copia temporal.
        parches = [mock.patch.object(sistema, "ARCHIVO", self.ruta_datos)]
        # Se fija la fecha en todos los módulos que puedan usarla. modelos se
        # incluye porque, después del Move Method, el cálculo de días vive ahí.
        for modulo in ("sistema.date", "modelos.date"):
            parches.append(mock.patch(modulo, fecha_fija(self.hoy), create=True))
        for parche in parches:
            parche.start()
            self.addCleanup(parche.stop)

    def ejecutar(self, *entradas):
        """Simula a una usuaria que escribe estas entradas en el menú.

        Al final escribe "0" para salir. Devuelve todo lo que se mostró
        en pantalla.
        """
        salida = io.StringIO()
        with mock.patch("builtins.input", side_effect=list(entradas) + ["0"]), redirect_stdout(salida):
            sistema.Sistema().menu()
        return salida.getvalue()

    def leer_datos(self):
        """Devuelve el contenido del archivo de datos después de operar."""
        with open(self.ruta_datos, encoding="utf-8") as archivo:
            return json.load(archivo)

    def solicitud_guardada(self, id_solicitud):
        for solicitud in self.leer_datos()["solicitudes"]:
            if solicitud["id"] == id_solicitud:
                return solicitud
        return None

    def assertMuestra(self, salida, texto_esperado):
        """Verifica que en pantalla aparezcan estas líneas, seguidas y en orden.

        Se ignoran las líneas en blanco.
        """
        def sin_blancos(texto):
            return "\n".join(linea for linea in texto.splitlines() if linea.strip())

        self.assertIn(sin_blancos(texto_esperado), sin_blancos(salida))


class PruebasReporte(PruebaBase):

    def test_reporte_completo(self):
        salida = self.ejecutar("7")
        self.assertMuestra(salida, """
============================================================
REPORTE DE SOLICITUDES - 16/11/2026
============================================================
Total de solicitudes: 9
Por estado:
  Pendientes: 3 (33.3%)
  En proceso: 3 (33.3%)
  Resueltas:  2 (22.2%)
  Rechazadas: 1 (11.1%)
Por tipo:
  CERTIFICADO: 3
  CAMBIO_COMISION: 2
  RECLAMO_NOTA: 2
  OTRO: 2
Por prioridad:
  Alta:  3
  Media: 4
  Baja:  2
Solicitudes vencidas: 5
  #2 CAMBIO_COMISION - Quiroga, Mateo
  #3 RECLAMO_NOTA - Ibarra, Valentina
  #4 OTRO - Ferrero, Lucia
  #5 CERTIFICADO - Benitez, Tomas
  #9 OTRO - Ibarra, Valentina
Carga abierta por responsable:
  Marcos Lugo: 1
  Sofia Arce: 1
  Diego Villalba: 1
============================================================
""")


class PruebasBusquedas(PruebaBase):

    def test_buscar_por_estado(self):
        salida = self.ejecutar("4", "PENDIENTE")
        self.assertMuestra(salida, """
#3 | RECLAMO_NOTA | Ibarra, Valentina | Alta | PENDIENTE | Sin asignar [VENCIDA]
#4 | OTRO | Ferrero, Lucia | Baja | PENDIENTE | Sin asignar [VENCIDA]
#7 | CAMBIO_COMISION | Mendez, Joaquin | Baja | PENDIENTE | Sin asignar
Total: 3
""")

    def test_buscar_por_tipo(self):
        salida = self.ejecutar("5", "CERTIFICADO")
        self.assertMuestra(salida, """
#1 | CERTIFICADO | Ferrero, Lucia | Media | RESUELTA | Ana Paredes (Bedelia)
#5 | CERTIFICADO | Benitez, Tomas | Media | EN_PROCESO | Sofia Arce (Secretaria de alumnos) [VENCIDA]
#8 | CERTIFICADO | Quiroga, Mateo | Alta | RESUELTA | Ana Paredes (Bedelia)
Total: 3
""")

    def test_buscar_por_estudiante(self):
        salida = self.ejecutar("6", "10001")
        self.assertMuestra(salida, """
#1 | CERTIFICADO | Ferrero, Lucia | Media | RESUELTA | Ana Paredes (Bedelia)
#4 | OTRO | Ferrero, Lucia | Baja | PENDIENTE | Sin asignar [VENCIDA]
Total: 2
""")

    def test_busqueda_sin_resultados(self):
        salida = self.ejecutar("4", "INEXISTENTE")
        self.assertMuestra(salida, "Total: 0")


# La solicitud #3 tiene prioridad alta y fecha 28/10/2026: vence cuando pasan MÁS de 5 días.

class PruebasVencimientoCon5Dias(PruebaBase):
    hoy = date(2026, 11, 2)  # pasaron 5 días

    def test_todavia_no_esta_vencida(self):
        salida = self.ejecutar("4", "PENDIENTE")
        self.assertMuestra(salida, "#3 | RECLAMO_NOTA | Ibarra, Valentina | Alta | PENDIENTE | Sin asignar")
        self.assertNotIn("Ibarra, Valentina | Alta | PENDIENTE | Sin asignar [VENCIDA]", salida)


class PruebasVencimientoCon6Dias(PruebaBase):
    hoy = date(2026, 11, 3)  # pasaron 6 días

    def test_ya_esta_vencida(self):
        salida = self.ejecutar("4", "PENDIENTE")
        self.assertMuestra(salida, "#3 | RECLAMO_NOTA | Ibarra, Valentina | Alta | PENDIENTE | Sin asignar [VENCIDA]")


class PruebasRegistrarSolicitud(PruebaBase):

    def test_registrar_con_estudiante_nuevo(self):
        salida = self.ejecutar(
            "1", "10007", "Laura", "Sosa", "laura.sosa@ejemplo.com", "TUP",
            "certificado", "Certificado de alumna regular", "2",
        )
        self.assertMuestra(salida, "Solicitud creada con id 10")

        datos = self.leer_datos()
        self.assertEqual(len(datos["solicitudes"]), 10)
        self.assertEqual(len(datos["estudiantes"]), 7)
        self.assertIn(
            {"legajo": "10007", "nombre": "Laura", "apellido": "Sosa",
             "email": "laura.sosa@ejemplo.com", "carrera": "TUP"},
            datos["estudiantes"],
        )
        self.assertEqual(self.solicitud_guardada(10), {
            "id": 10, "legajo": "10007", "tipo": "CERTIFICADO",
            "descripcion": "Certificado de alumna regular", "prioridad": 2,
            "estado": "PENDIENTE", "fecha": "2026-11-16", "responsable": None,
        })

    def test_registrar_con_estudiante_existente_no_pide_sus_datos(self):
        # Con un legajo que ya existe, el menú no pide nombre, apellido, email ni carrera.
        salida = self.ejecutar("1", "10001", "OTRO", "Consulta por mesa especial", "3")
        self.assertMuestra(salida, "Estudiante: Ferrero, Lucia")
        self.assertMuestra(salida, "Solicitud creada con id 10")
        datos = self.leer_datos()
        self.assertEqual(len(datos["estudiantes"]), 6)
        self.assertEqual(self.solicitud_guardada(10)["legajo"], "10001")

    def test_tipo_invalido_no_crea_la_solicitud(self):
        salida = self.ejecutar("1", "10001", "BECA", "Pedido de beca", "2")
        self.assertMuestra(salida, "Tipo invalido")
        self.assertEqual(len(self.leer_datos()["solicitudes"]), 9)

    def test_prioridad_fuera_de_rango_se_guarda_como_media(self):
        self.ejecutar("1", "10001", "OTRO", "Consulta", "7")
        self.assertEqual(self.solicitud_guardada(10)["prioridad"], 2)


class PruebasAsignarResponsable(PruebaBase):

    def test_asignar_responsable(self):
        salida = self.ejecutar("3", "3", "1")
        self.assertMuestra(salida, "Responsable asignado")
        self.assertEqual(self.solicitud_guardada(3)["responsable"], 1)

    def test_no_se_asigna_a_una_solicitud_cerrada(self):
        salida = self.ejecutar("3", "1", "2")  # la #1 está RESUELTA
        self.assertMuestra(salida, "La solicitud ya esta cerrada")
        self.assertEqual(self.solicitud_guardada(1)["responsable"], 1)

    def test_responsable_inexistente(self):
        salida = self.ejecutar("3", "3", "99")
        self.assertMuestra(salida, "No existe el responsable")
        self.assertIsNone(self.solicitud_guardada(3)["responsable"])

    def test_solicitud_inexistente(self):
        salida = self.ejecutar("3", "99", "1")
        self.assertMuestra(salida, "No existe la solicitud")


class PruebasCambiarEstado(PruebaBase):

    def test_de_en_proceso_a_resuelta(self):
        salida = self.ejecutar("2", "2", "RESUELTA")
        self.assertMuestra(salida, "Estado actualizado")
        self.assertEqual(self.solicitud_guardada(2)["estado"], "RESUELTA")

    def test_de_pendiente_a_rechazada(self):
        salida = self.ejecutar("2", "3", "RECHAZADA")
        self.assertMuestra(salida, "Estado actualizado")
        self.assertEqual(self.solicitud_guardada(3)["estado"], "RECHAZADA")

    def test_no_pasa_a_en_proceso_sin_responsable(self):
        salida = self.ejecutar("2", "3", "EN_PROCESO")
        self.assertMuestra(salida, "Debe asignar un responsable primero")
        self.assertEqual(self.solicitud_guardada(3)["estado"], "PENDIENTE")

    def test_pasa_a_en_proceso_despues_de_asignar(self):
        salida = self.ejecutar("3", "3", "1", "2", "3", "EN_PROCESO")
        self.assertMuestra(salida, "Estado actualizado")
        self.assertEqual(self.solicitud_guardada(3)["estado"], "EN_PROCESO")

    def test_no_salta_de_pendiente_a_resuelta(self):
        salida = self.ejecutar("2", "3", "RESUELTA")
        self.assertMuestra(salida, "Cambio de estado no permitido")
        self.assertEqual(self.solicitud_guardada(3)["estado"], "PENDIENTE")

    def test_una_solicitud_cerrada_no_cambia(self):
        salida = self.ejecutar("2", "1", "RECHAZADA")  # la #1 está RESUELTA
        self.assertMuestra(salida, "Cambio de estado no permitido")
        self.assertEqual(self.solicitud_guardada(1)["estado"], "RESUELTA")

    def test_solicitud_inexistente(self):
        salida = self.ejecutar("2", "99", "RESUELTA")
        self.assertMuestra(salida, "No existe la solicitud")


class PruebasMenu(PruebaBase):

    def test_opcion_invalida(self):
        salida = self.ejecutar("9")
        self.assertMuestra(salida, "Opcion invalida")

    def test_listar_responsables(self):
        salida = self.ejecutar("8")
        self.assertMuestra(salida, """
  1. Ana Paredes (Bedelia)
  2. Marcos Lugo (Coordinacion academica)
  3. Sofia Arce (Secretaria de alumnos)
  4. Diego Villalba (Tutoria)
""")


if __name__ == "__main__":
    unittest.main()
