from Animales import Mascota


class Consulta:
    """
    Clase que representa una consulta veterinaria en la Clínica "Amigos Peludos".

    Esta clase almacena toda la información relevante de cada visita médica,
    incluyendo la fecha de atención, el motivo de la consulta, el diagnóstico
    realizado por el veterinario y la mascota que fue atendida.

    Attributes:
        fecha (str): Fecha en que se realizó la consulta veterinaria
        motivo (str): Razón o síntomas por los que se trae a la mascota
        diagnostico (str): Evaluación y conclusión médica del veterinario
        mascota_relacionada (str): Nombre de la mascota que recibió la atención
    """

    def __init__(self, fecha, motivo, diagnostico, mascota_relacionada):
        """
        Inicializa una nueva consulta veterinaria con todos sus detalles.

        Args:
            fecha (str): Fecha de la consulta (formato libre para flexibilidad)
            motivo (str): Descripción del motivo de la visita o síntomas presentados
            diagnostico (str): Conclusión médica y tratamiento recomendado
            mascota_relacionada (str): Nombre de la mascota atendida en la consulta

        Ejemplo:
            consulta = Consulta("01/01/2024", "Vómitos y diarrea",
                              "Gastritis aguda", "Firulais")
        """
        self.fecha = fecha
        self.motivo = motivo
        self.diagnostico = diagnostico
        self.mascota_relacionada = mascota_relacionada

    def __str__(self):
        """
        Genera una representación en texto de la consulta veterinaria.

        Returns:
            str: Cadena formateada con todos los detalles de la consulta,
                 incluyendo fecha, motivo, diagnóstico y mascota atendida.
                 Cada dato se presenta en una línea separada para mejor lectura.

        Ejemplo de salida:
            01/01/2024
            Vómitos y diarrea
            Gastritis aguda
            Firulais
        """
        return (f"{self.fecha}\n "
                f"{self.motivo}\n "
                f"{self.diagnostico}\n "
                f"{self.mascota_relacionada}")