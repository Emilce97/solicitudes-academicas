from datetime import datetime, date

# Prioridades de una solicitud (1 = la más urgente).
PRIORIDAD_ALTA = 1
PRIORIDAD_MEDIA = 2
PRIORIDAD_BAJA = 3

# Días que puede estar abierta una solicitud antes de considerarse vencida.
PLAZO_ALTA = 5
PLAZO_MEDIA = 10
PLAZO_BAJA = 20


class Estudiante:
    def __init__(self, legajo, nombre, apellido, email, carrera):
        self.legajo = legajo
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.carrera = carrera


class Responsable:
    def __init__(self, id, nombre, area):
        self.id = id
        self.nombre = nombre
        self.area = area


class Solicitud:
    def __init__(self, id, estudiante, tipo, descripcion, prioridad, estado, fecha, responsable=None):
        self.id = id
        self.estudiante = estudiante
        self.tipo = tipo
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.estado = estado
        self.fecha = fecha
        self.responsable = responsable

    def dias_transcurridos(self):
        f = datetime.strptime(self.fecha, "%Y-%m-%d").date()
        return (date.today() - f).days

    def esta_vencida(self):
        if self.estado == "RESUELTA" or self.estado == "RECHAZADA":
            return False
        if self.prioridad == PRIORIDAD_ALTA:
            return self.dias_transcurridos() > PLAZO_ALTA
        elif self.prioridad == PRIORIDAD_MEDIA:
            return self.dias_transcurridos() > PRIORIDAD_MEDIA
        else:
            return self.dias_transcurridos() > PLAZO_BAJA