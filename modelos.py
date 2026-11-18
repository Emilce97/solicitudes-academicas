from datetime import datetime, date

# Prioridades de una solicitud (1 = la más urgente).
PRIORIDAD_ALTA = 1
PRIORIDAD_MEDIA = 2
PRIORIDAD_BAJA = 3

# Días que puede estar abierta una solicitud antes de considerarse vencida.
PLAZO_ALTA = 5
PLAZO_MEDIA = 10
PLAZO_BAJA = 20

# Estados de una solicitud
ESTADO_PENDIENTE = "PENDIENTE"
ESTADO_EN_PROCESO = "EN_PROCESO"
ESTADO_RESUELTA = "RESUELTA"
ESTADO_RECHAZADA = "RECHAZADA"

# Tipos de solicitud válidos.
TIPOS_VALIDOS = ("CERTIFICADO", "CAMBIO_COMISION", "RECLAMO_NOTA", "OTRO")


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
        fecha_alta = datetime.strptime(self.fecha, "%Y-%m-%d").date()
        return (date.today() - fecha_alta).days

    def esta_vencida(self):
        if self.estado == ESTADO_RESUELTA or self.estado == ESTADO_RECHAZADA:
            return False
        if self.prioridad == PRIORIDAD_ALTA:
            return self.dias_transcurridos() > PLAZO_ALTA
        elif self.prioridad == PRIORIDAD_MEDIA:
            return self.dias_transcurridos() > PLAZO_MEDIA
        else:
            return self.dias_transcurridos() > PLAZO_BAJA
