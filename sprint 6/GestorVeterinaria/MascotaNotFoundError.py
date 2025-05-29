class MascotaNotFoundError(Exception):
    """
       Clase personalizada para manejar errores relacionados con la busqueda de objetos de la aplicación.

       Attributes:
           message -- explicación del error
       """

    def __init__(self, mensaje):
        self.mensaje = mensaje

    def __str__(self):
        return self.mensaje