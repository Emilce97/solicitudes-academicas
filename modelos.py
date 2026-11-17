from datetime import datetime, date


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
        if self.prioridad == 1:
            return self.dias_transcurridos() > 5
        elif self.prioridad == 2:
            return self.dias_transcurridos() > 10
        else:
            return self.dias_transcurridos() > 20