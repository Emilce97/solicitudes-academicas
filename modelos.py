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
