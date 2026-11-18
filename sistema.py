import json
from datetime import date
from modelos import (Estudiante, Responsable, Solicitud,
                     PRIORIDAD_ALTA, PRIORIDAD_MEDIA, PRIORIDAD_BAJA,
                     ESTADO_PENDIENTE, ESTADO_EN_PROCESO, ESTADO_RESUELTA, ESTADO_RECHAZADA,
                     TIPOS_VALIDOS)

ARCHIVO = "datos.json"


class Sistema:
    def __init__(self):
        self.solicitudes = []
        self.estudiantes = []
        self.responsables = []
        self.cargar()

    # ------------------------------------------------------------------
    # Persistencia
    # ------------------------------------------------------------------
    def cargar(self):
        try:
            archivo = open(ARCHIVO, "r", encoding="utf-8")
            datos = json.load(archivo)
            archivo.close()
            for e in datos["estudiantes"]:
                self.estudiantes.append(Estudiante(e["legajo"], e["nombre"], e["apellido"], e["email"], e["carrera"]))
            for r in datos["responsables"]:
                self.responsables.append(Responsable(r["id"], r["nombre"], r["area"]))
            for s in datos["solicitudes"]:
                estudiante = None
                for e in self.estudiantes:
                    if e.legajo == s["legajo"]:
                        estudiante = e
                r = None
                for x in self.responsables:
                    if x.id == s["responsable"]:
                        r = x
                self.solicitudes.append(Solicitud(s["id"], estudiante, s["tipo"], s["descripcion"], s["prioridad"], s["estado"], s["fecha"], r))
        except:
            pass

    def guardar(self):
        datos = {"estudiantes": [], "responsables": [], "solicitudes": []}
        for e in self.estudiantes:
            datos["estudiantes"].append({"legajo": e.legajo, "nombre": e.nombre, "apellido": e.apellido,
                                         "email": e.email, "carrera": e.carrera})
        for r in self.responsables:
            datos["responsables"].append({"id": r.id, "nombre": r.nombre, "area": r.area})
        for s in self.solicitudes:
            id_responsable = None
            if s.responsable != None:
                id_responsable = s.responsable.id
            datos["solicitudes"].append({"id": s.id, "legajo": s.estudiante.legajo, "tipo": s.tipo,
                                         "descripcion": s.descripcion, "prioridad": s.prioridad,
                                         "estado": s.estado, "fecha": s.fecha, "responsable": id_responsable})
        archivo = open(ARCHIVO, "w", encoding="utf-8")
        json.dump(datos, archivo, indent=2, ensure_ascii=False)
        archivo.close()

    # ------------------------------------------------------------------
    # Operaciones
    # ------------------------------------------------------------------
    def crear_solicitud(self, estudiante, tipo, descripcion, prioridad):
        if tipo not in TIPOS_VALIDOS:
            print("Tipo invalido")
            return None
        estudiante_encontrado = None
        for e in self.estudiantes:
            if e.legajo == estudiante.legajo:
                estudiante_encontrado = e
        if estudiante_encontrado == None:
            estudiante_encontrado = estudiante
            self.estudiantes.append(estudiante_encontrado)
        if prioridad < PRIORIDAD_ALTA or prioridad > PRIORIDAD_BAJA:
            prioridad = PRIORIDAD_MEDIA
        nuevo_id = 1
        for s in self.solicitudes:
            if s.id >= nuevo_id:
                nuevo_id = s.id + 1
        hoy = date.today().isoformat()
        s = Solicitud(nuevo_id, estudiante_encontrado, tipo, descripcion, prioridad, ESTADO_PENDIENTE, hoy)
        self.solicitudes.append(s)
        self.guardar()
        print("Solicitud creada con id", nuevo_id)
        return s

    def cambiar_estado(self, id_solicitud, nuevo_estado):
        s = None
        for x in self.solicitudes:
            if x.id == id_solicitud:
                s = x
        if s == None:
            print("No existe la solicitud")
            return
        if nuevo_estado == ESTADO_EN_PROCESO and s.responsable == None:
            print("Debe asignar un responsable primero")
            return
        if s.estado == ESTADO_PENDIENTE and (nuevo_estado == ESTADO_EN_PROCESO or nuevo_estado == ESTADO_RECHAZADA):
            s.estado = nuevo_estado
        elif s.estado == ESTADO_EN_PROCESO and (nuevo_estado == ESTADO_RESUELTA or nuevo_estado == ESTADO_RECHAZADA):
            s.estado = nuevo_estado
        else:
            print("Cambio de estado no permitido")
            return
        self.guardar()
        print("Estado actualizado")

    def asignar_responsable(self, id_solicitud, id_responsable):
        s = None
        for x in self.solicitudes:
            if x.id == id_solicitud:
                s = x
        if s == None:
            print("No existe la solicitud")
            return
        r = None
        for x in self.responsables:
            if x.id == id_responsable:
                r = x
        if r == None:
            print("No existe el responsable")
            return
        if s.estado == ESTADO_RESUELTA or s.estado == ESTADO_RECHAZADA:
            print("La solicitud ya esta cerrada")
            return
        s.responsable = r
        self.guardar()
        print("Responsable asignado")

    # ------------------------------------------------------------------
    # Busquedas
    # ------------------------------------------------------------------
    def _texto_solicitud(self, s):
        texto_responsable = "Sin asignar"
        if s.responsable != None:
            texto_responsable = s.responsable.nombre + " (" + s.responsable.area + ")"
        texto_prioridad = "Alta" if s.prioridad == PRIORIDAD_ALTA else ("Media" if s.prioridad == PRIORIDAD_MEDIA else "Baja")
        marca_vencida = " [VENCIDA]" if s.esta_vencida() else ""
        return ("#" + str(s.id) + " | " + s.tipo + " | " + s.estudiante.apellido + ", " + s.estudiante.nombre
                + " | " + texto_prioridad + " | " + s.estado + " | " + texto_responsable + marca_vencida)

    def _mostrar_solicitudes(self, resultados):
        for s in resultados:
            print(self._texto_solicitud(s))
        print("Total:", len(resultados))

    def buscar_por_estado(self, estado):
        resultados = []
        for s in self.solicitudes:
            if s.estado == estado:
                resultados.append(s)
        self._mostrar_solicitudes(resultados)
        return resultados

    def buscar_por_tipo(self, tipo):
        resultados = []
        for s in self.solicitudes:
            if s.tipo == tipo:
                resultados.append(s)
        self._mostrar_solicitudes(resultados)
        return resultados

    def buscar_por_estudiante(self, legajo):
        resultados = []
        for s in self.solicitudes:
            if s.estudiante.legajo == legajo:
                resultados.append(s)
        self._mostrar_solicitudes(resultados)
        return resultados

    # ------------------------------------------------------------------
    # Reporte
    # ------------------------------------------------------------------
    def _contar_por_estado(self):
        pendientes = 0
        en_proceso = 0
        resueltas = 0
        rechazadas = 0
        for s in self.solicitudes:
            if s.estado == ESTADO_PENDIENTE:
                pendientes += 1
            elif s.estado == ESTADO_EN_PROCESO:
                en_proceso += 1
            elif s.estado == ESTADO_RESUELTA:
                resueltas += 1
            elif s.estado == ESTADO_RECHAZADA:
                rechazadas += 1
        return pendientes, en_proceso, resueltas, rechazadas

    def _contar_por_tipo(self):
        por_tipo = {}
        for s in self.solicitudes:
            if s.tipo in por_tipo:
                por_tipo[s.tipo] += 1
            else:
                por_tipo[s.tipo] = 1
        return por_tipo

    def _contar_por_prioridad(self):
        alta = 0
        media = 0
        baja = 0
        for s in self.solicitudes:
            if s.prioridad == PRIORIDAD_ALTA:
                alta += 1
            elif s.prioridad == PRIORIDAD_MEDIA:
                media += 1
            else:
                baja += 1
        return alta, media, baja

    def _solicitudes_vencidas(self):
        vencidas = []
        for s in self.solicitudes:
            if s.esta_vencida():
                vencidas.append(s)
        return vencidas

    def _carga_abierta_por_responsable(self):
        carga = {}
        for s in self.solicitudes:
            if s.responsable != None and s.estado != ESTADO_RESUELTA and s.estado != ESTADO_RECHAZADA:
                if s.responsable.nombre in carga:
                    carga[s.responsable.nombre] += 1
                else:
                    carga[s.responsable.nombre] = 1
        return carga

    def reporte(self):
        print("=" * 60)
        print("REPORTE DE SOLICITUDES - " + date.today().strftime("%d/%m/%Y"))
        print("=" * 60)
        total = len(self.solicitudes)
        print("Total de solicitudes:", total)
        if total == 0:
            print("No hay solicitudes cargadas")
            return
        pendientes, en_proceso, resueltas, rechazadas = self._contar_por_estado()
        print("\nPor estado:")
        print("  Pendientes: " + str(pendientes) + " (" + str(round(pendientes * 100 / total, 1)) + "%)")
        print("  En proceso: " + str(en_proceso) + " (" + str(round(en_proceso * 100 / total, 1)) + "%)")
        print("  Resueltas:  " + str(resueltas) + " (" + str(round(resueltas * 100 / total, 1)) + "%)")
        print("  Rechazadas: " + str(rechazadas) + " (" + str(round(rechazadas * 100 / total, 1)) + "%)")
        por_tipo = self._contar_por_tipo()
        print("\nPor tipo:")
        for k in por_tipo:
            print("  " + k + ": " + str(por_tipo[k]))
        alta, media, baja = self._contar_por_prioridad()
        print("\nPor prioridad:")
        print("  Alta:  " + str(alta))
        print("  Media: " + str(media))
        print("  Baja:  " + str(baja))
        vencidas = self._solicitudes_vencidas()
        print("\nSolicitudes vencidas: " + str(len(vencidas)))
        for s in vencidas:
            print("  #" + str(s.id) + " " + s.tipo + " - " + s.estudiante.apellido + ", " + s.estudiante.nombre)
        carga = self._carga_abierta_por_responsable()
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
                estudiante = None
                for e in self.estudiantes:
                    if e.legajo == legajo:
                        estudiante = e
                if estudiante == None:
                    nombre = input("Nombre: ")
                    apellido = input("Apellido: ")
                    email = input("Email: ")
                    carrera = input("Carrera: ")
                    estudiante = Estudiante(legajo, nombre, apellido, email, carrera)
                else:
                    print("Estudiante: " + estudiante.apellido + ", " + estudiante.nombre)
                tipo = input("Tipo (CERTIFICADO, CAMBIO_COMISION, RECLAMO_NOTA, OTRO): ").upper()
                descripcion = input("Descripcion: ")
                prioridad = int(input("Prioridad (1=Alta, 2=Media, 3=Baja): "))
                self.crear_solicitud(estudiante, tipo, descripcion, prioridad)
            elif op == "2":
                id_solicitud = int(input("Id de solicitud: "))
                nuevo_estado = input("Nuevo estado (EN_PROCESO, RESUELTA, RECHAZADA): ").upper()
                self.cambiar_estado(id_solicitud, nuevo_estado)
            elif op == "3":
                id_solicitud = int(input("Id de solicitud: "))
                for r in self.responsables:
                    print("  " + str(r.id) + ". " + r.nombre + " (" + r.area + ")")
                id_responsable = int(input("Id de responsable: "))
                self.asignar_responsable(id_solicitud, id_responsable)
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
                for r in self.responsables:
                    print("  " + str(r.id) + ". " + r.nombre + " (" + r.area + ")")
            elif op == "0":
                print("Hasta luego")
                break
            else:
                print("Opcion invalida")
