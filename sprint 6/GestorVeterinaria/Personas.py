from Animales import Mascota


class Duenho:
    """
    Clase que representa al dueño de una mascota.
    Almacena la información de contacto de los propietarios.
    """

    def __init__(self, nombre_duenho, telefono, direccion):
        """
        Inicializa un nuevo dueño con sus datos de contacto.

        Args:
            nombre_duenho (str): Nombre del propietario
            telefono (str): Número de contacto
            direccion (str): Dirección del domicilio
        """
        self.nombre_duenho = nombre_duenho
        self.telefono = telefono
        self.direccion = direccion

    def __str__(self):
        """
        Retorna una representación en string del dueño.

        Returns:
            str: Información formateada del dueño
        """
        return (f"Nombre: {self.nombre_duenho}\n "
                f"Telefono: {self.telefono}\n"
                f"Direccion: {self.direccion}")