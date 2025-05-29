import csv
class Mascota:
    """
    Clase que representa una mascota en la Clínica Veterinaria.
    Almacena la información básica de cada paciente animal.
    """

    def __init__(self, nombre_mascota, especie, raza, edad, duenho):
        """
        Inicializa una nueva mascota con sus atributos básicos.

        Args:
            nombre_mascota (str): Nombre de la mascota
            especie (str): Tipo de animal (ej: perro, gato, etc.)
            raza (str): Raza específica de la mascota
            edad (str): Edad de la mascota
            duenho (str): Nombre del dueño de la mascota
        """
        self.nombre_mascota = nombre_mascota
        self.especie = especie
        self.raza = raza
        self.edad = int(edad)
        self.duenho = duenho

    def __str__(self):
        """
        Retorna una representación en string de la mascota.

        Returns:
            str: Información formateada de la mascota
        """
        return (f"Nombre: {self.nombre_mascota}\n "
                f"Especie: {self.especie}\n "
                f"Raza: {self.raza}\n "
                f"Edad: {self.edad} años\n "
                f"Dueño: {self.duenho}")
    
    