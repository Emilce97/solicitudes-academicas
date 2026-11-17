import json
from datetime import datetime, date
from modelos import Estudiante, Responsable, Solicitud

ARCHIVO = "datos.json"


class Sistema:
    def __init__(self):
        self.lst = []
        self.estudiantes = []
        self.resp = []
        self.cargar()

    # ------------------------------------------------------------------
    # Persistencia
    # ------------------------------------------------------------------
    def cargar(self):
        try:
            f = open(ARCHIVO, "r", encoding="utf-8")
            d = json.load(f)
            f.close()
            for e in d["estudiantes"]:
                self.estudiantes.append(Estudiante(e["legajo"], e["nombre"], e["apellido"], e["email"], e["carrera"]))
            for r in d["responsables"]:
                self.resp.append(Responsable(r["id"], r["nombre"], r["area"]))
            for s in d["solicitudes"]:
                est = None
                for e in self.estudiantes:
                    if e.legajo == s["legajo"]:
                        est = e
                r = None
                for x in self.resp:
                    if x.id == s["responsable"]:
                        r = x
                self.lst.append(Solicitud(s["id"], est, s["tipo"], s["descripcion"], s["prioridad"], s["estado"], s["fecha"], r))
        except:
            pass

    def guardar(self):
        d = {"estudiantes": [], "responsables": [], "solicitudes": []}
        for e in self.estudiantes:
            d["estudiantes"].append({"legajo": e.legajo, "nombre": e.nombre, "apellido": e.apellido,
                                     "email": e.email, "carrera": e.carrera})
        for r in self.resp:
            d["responsables"].append({"id": r.id, "nombre": r.nombre, "area": r.area})
        for s in self.lst:
            rid = None
            if s.responsable != None:
                rid = s.responsable.id
            d["solicitudes"].append({"id": s.id, "legajo": s.estudiante.legajo, "tipo": s.tipo,
                                     "descripcion": s.descripcion, "prioridad": s.prioridad,
                                     "estado": s.estado, "fecha": s.fecha, "responsable": rid})
        f = open(ARCHIVO, "w", encoding="utf-8")
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.close()

    # ------------------------------------------------------------------
    # Operaciones
    # ------------------------------------------------------------------
    def crear_solicitud(self, legajo, nombre, apellido, email, carrera, tipo, descripcion, prioridad):
        if tipo != "CERTIFICADO" and tipo != "CAMBIO_COMISION" and tipo != "RECLAMO_NOTA" and tipo != "OTRO":
            print("Tipo invalido")
            return None
        est = None
        for e in self.estudiantes:
            if e.legajo == legajo:
                est = e
        if est == None:
            est = Estudiante(legajo, nombre, apellido, email, carrera)
            self.estudiantes.append(est)
        if prioridad < 1 or prioridad > 3:
            prioridad = 2
        id = 1
        for s in self.lst:
            if s.id >= id:
                id = s.id + 1
        hoy = date.today().isoformat()
        s = Solicitud(id, est, tipo, descripcion, prioridad, "PENDIENTE", hoy)
        self.lst.append(s)
        self.guardar()
        print("Solicitud creada con id", id)
        return s

    def cambiar_estado(self, id, nuevo):
        s = None
        for x in self.lst:
            if x.id == id:
                s = x
        if s == None:
            print("No existe la solicitud")
            return
        if nuevo == "EN_PROCESO" and s.responsable == None:
            print("Debe asignar un responsable primero")
            return
        if s.estado == "PENDIENTE" and (nuevo == "EN_PROCESO" or nuevo == "RECHAZADA"):
            s.estado = nuevo
        elif s.estado == "EN_PROCESO" and (nuevo == "RESUELTA" or nuevo == "RECHAZADA"):
            s.estado = nuevo
        else:
            print("Cambio de estado no permitido")
            return
        self.guardar()
        print("Estado actualizado")

    def asignar_responsable(self, id, id_resp):
        s = None
        for x in self.lst:
            if x.id == id:
                s = x
        if s == None:
            print("No existe la solicitud")
            return
        r = None
        for x in self.resp:
            if x.id == id_resp:
                r = x
        if r == None:
            print("No existe el responsable")
            return
        if s.estado == "RESUELTA" or s.estado == "RECHAZADA":
            print("La solicitud ya esta cerrada")
            return
        s.responsable = r
        self.guardar()
        print("Responsable asignado")

    # ------------------------------------------------------------------
    # Busquedas
    # ------------------------------------------------------------------
    def _texto_solicitud(self, s):
        r = "Sin asignar"
        if s.responsable != None:
            r = s.responsable.nombre + " (" + s.responsable.area + ")"
        p = "Alta" if s.prioridad == 1 else ("Media" if s.prioridad == 2 else "Baja")
        v = " [VENCIDA]" if s.esta_vencida() else ""
        return ("#" + str(s.id) + " | " + s.tipo + " | " + s.estudiante.apellido + ", " + s.estudiante.nombre
                + " | " + p + " | " + s.estado + " | " + r + v)

    def _mostrar_solicitudes(self, res):
        for s in res:
            print(self._texto_solicitud(s))
        print("Total:", len(res))

    def buscar_por_estado(self, estado):
        res = []
        for s in self.lst:
            if s.estado == estado:
                res.append(s)
        self._mostrar_solicitudes(res)
        return res

    def buscar_por_tipo(self, tipo):
        res = []
        for s in self.lst:
            if s.tipo == tipo:
                res.append(s)
        self._mostrar_solicitudes(res)
        return res

    def buscar_por_estudiante(self, legajo):
        res = []
        for s in self.lst:
            if s.estudiante.legajo == legajo:
                res.append(s)
        self._mostrar_solicitudes(res)
        return res

    # ------------------------------------------------------------------
    # Reporte
    # ------------------------------------------------------------------
    def _contar_por_estado(self):
        c1 = 0
        c2 = 0
        c3 = 0
        c4 = 0
        for s in self.lst:
            if s.estado == "PENDIENTE":
                c1 += 1
            elif s.estado == "EN_PROCESO":
                c2 += 1
            elif s.estado == "RESUELTA":
                c3 += 1
            elif s.estado == "RECHAZADA":
                c4 += 1
        return c1, c2, c3, c4

    def reporte(self):
        print("=" * 60)
        print("REPORTE DE SOLICITUDES - " + date.today().strftime("%d/%m/%Y"))
        print("=" * 60)
        total = len(self.lst)
        print("Total de solicitudes:", total)
        if total == 0:
            print("No hay solicitudes cargadas")
            return
        c1, c2, c3, c4 = self._contar_por_estado()
        print("\nPor estado:")
        print("  Pendientes: " + str(c1) + " (" + str(round(c1 * 100 / total, 1)) + "%)")
        print("  En proceso: " + str(c2) + " (" + str(round(c2 * 100 / total, 1)) + "%)")
        print("  Resueltas:  " + str(c3) + " (" + str(round(c3 * 100 / total, 1)) + "%)")
        print("  Rechazadas: " + str(c4) + " (" + str(round(c4 * 100 / total, 1)) + "%)")
        t = {}
        for s in self.lst:
            if s.tipo in t:
                t[s.tipo] += 1
            else:
                t[s.tipo] = 1
        print("\nPor tipo:")
        for k in t:
            print("  " + k + ": " + str(t[k]))
        a = 0
        m = 0
        b = 0
        for s in self.lst:
            if s.prioridad == 1:
                a += 1
            elif s.prioridad == 2:
                m += 1
            else:
                b += 1
        print("\nPor prioridad:")
        print("  Alta:  " + str(a))
        print("  Media: " + str(m))
        print("  Baja:  " + str(b))
        v = []
        for s in self.lst:
            if s.estado != "RESUELTA" and s.estado != "RECHAZADA":
                f = datetime.strptime(s.fecha, "%Y-%m-%d").date()
                d = (date.today() - f).days
                if (s.prioridad == 1 and d > 5) or (s.prioridad == 2 and d > 10) or (s.prioridad == 3 and d > 20):
                    v.append(s)
        print("\nSolicitudes vencidas: " + str(len(v)))
        for s in v:
            print("  #" + str(s.id) + " " + s.tipo + " - " + s.estudiante.apellido + ", " + s.estudiante.nombre)
        carga = {}
        for s in self.lst:
            if s.responsable != None and s.estado != "RESUELTA" and s.estado != "RECHAZADA":
                if s.responsable.nombre in carga:
                    carga[s.responsable.nombre] += 1
                else:
                    carga[s.responsable.nombre] = 1
        print("\nCarga abierta por responsable:")
        if len(carga) == 0:
            print("  (ninguna)")
        for k in carga:
            print("  " + k + ": " + str(carga[k]))
        print("=" * 60)

    # ------------------------------------------------------------------
    # Menu de consola
    # ------------------------------------------------------------------
    def menu(self):
        while True:
            print("\n--- GESTION DE SOLICITUDES ACADEMICAS ---")
            print("1. Registrar solicitud")
            print("2. Cambiar estado")
            print("3. Asignar responsable")
            print("4. Buscar por estado")
            print("5. Buscar por tipo")
            print("6. Buscar por estudiante")
            print("7. Reporte")
            print("8. Listar responsables")
            print("0. Salir")
            op = input("Opcion: ")
            if op == "1":
                legajo = input("Legajo: ")
                est = None
                for e in self.estudiantes:
                    if e.legajo == legajo:
                        est = e
                if est == None:
                    nombre = input("Nombre: ")
                    apellido = input("Apellido: ")
                    email = input("Email: ")
                    carrera = input("Carrera: ")
                else:
                    nombre = est.nombre
                    apellido = est.apellido
                    email = est.email
                    carrera = est.carrera
                    print("Estudiante: " + apellido + ", " + nombre)
                tipo = input("Tipo (CERTIFICADO, CAMBIO_COMISION, RECLAMO_NOTA, OTRO): ").upper()
                descripcion = input("Descripcion: ")
                prioridad = int(input("Prioridad (1=Alta, 2=Media, 3=Baja): "))
                self.crear_solicitud(legajo, nombre, apellido, email, carrera, tipo, descripcion, prioridad)
            elif op == "2":
                id = int(input("Id de solicitud: "))
                nuevo = input("Nuevo estado (EN_PROCESO, RESUELTA, RECHAZADA): ").upper()
                self.cambiar_estado(id, nuevo)
            elif op == "3":
                id = int(input("Id de solicitud: "))
                for r in self.resp:
                    print("  " + str(r.id) + ". " + r.nombre + " (" + r.area + ")")
                id_resp = int(input("Id de responsable: "))
                self.asignar_responsable(id, id_resp)
            elif op == "4":
                estado = input("Estado (PENDIENTE, EN_PROCESO, RESUELTA, RECHAZADA): ").upper()
                self.buscar_por_estado(estado)
            elif op == "5":
                tipo = input("Tipo (CERTIFICADO, CAMBIO_COMISION, RECLAMO_NOTA, OTRO): ").upper()
                self.buscar_por_tipo(tipo)
            elif op == "6":
                legajo = input("Legajo: ")
                self.buscar_por_estudiante(legajo)
            elif op == "7":
                self.reporte()
            elif op == "8":
                for r in self.resp:
                    print("  " + str(r.id) + ". " + r.nombre + " (" + r.area + ")")
            elif op == "0":
                print("Hasta luego")
                break
            else:
                print("Opcion invalida")
