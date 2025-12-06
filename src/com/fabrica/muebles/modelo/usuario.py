from datetime import date


class Usuario:
    """Clase modelo para Usuario del sistema"""

    def __init__(self, id_usuario=None, usuario=None, password=None,
                 rol=None, email=None, fecha_registro=None, estado=1):
        self.id_usuario = id_usuario
        self.usuario = usuario
        self.password = password
        self.rol = rol
        self.email = email
        self.fecha_registro = fecha_registro or date.today()
        self.estado = estado

    def __str__(self):
        return f"Usuario{{usuario='{self.usuario}', rol='{self.rol}'}}"