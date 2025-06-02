
import datetime
from Controller import *

class Mascota:  
    """
    Clase que representa una mascota en la Clínica Veterinaria.
    Almacena la información básica de cada paciente animal.
    """
    #Inicializa una nueva mascota con sus atributos básicos.
    def __init__(self, nombre_mascota, especie, raza, edad, duenho):
      
        self.nombre_mascota = nombre_mascota
        self.especie = especie
        self.raza = raza
        self.validar_edad(edad)
        self.edad = edad
        self.duenho = duenho

    
    #Retorna una representación en string de la mascota. 
    def __str__(self):
       
        return (f"Nombre: {self.nombre_mascota}\n "
                f"Especie: {self.especie}\n "
                f"Raza: {self.raza}\n "
                f"Edad: {self.edad} años\n "
                f"Dueño: {self.duenho}")
    
    @staticmethod
    def validar_edad(edad):
        if not str(edad).isnumeric() or int(edad) < 0:
            raise ValueError("La edad debe ser un valor numérico positivo")
        return True


class Duenho:
    """
    Clase que representa al dueño de una mascota.
    Almacena la información de contacto de los propietarios.
    """
    #Inicializa un nuevo dueño con sus datos de contacto.
    def __init__(self, nombre_duenho, telefono, direccion):
       
        self.nombre_duenho = nombre_duenho
        self.validar_telefono(telefono)
        self.telefono = telefono
        self.direccion = direccion
  
   #Retorna una representación en string del dueño.
    def __str__(self):
       
        return (f"Nombre: {self.nombre_duenho}\n "
                f"Telefono: {self.telefono}\n"
                f"Direccion: {self.direccion}")
    @staticmethod
    def validar_telefono(telefono):
        if not str(telefono).isnumeric() or int(telefono) < 0:
            raise ValueError("El telefono debe ser un valor numérico positivo")
        return True

class Consulta:
    """
    Clase que representa una consulta veterinaria en la Clínica "Amigos Peludos".

    Esta clase almacena toda la información relevante de cada visita médica,
    incluyendo la fecha de atención, el motivo de la consulta, el diagnóstico
    realizado por el veterinario y la mascota que fue atendida.
    """

    #Inicializa una nueva consulta veterinaria con todos sus detalles.
    def __init__(self, fecha, motivo, diagnostico, mascota_relacionada):
       
        self.validar_fecha(fecha)
        self.fecha = fecha
        self.motivo = motivo
        self.diagnostico = diagnostico
        self.mascota_relacionada = mascota_relacionada
    
    #Genera una representación en texto de la consulta veterinaria.
    def __str__(self):
        
        return (f"{self.fecha}\n "
                f"{self.motivo}\n "
                f"{self.diagnostico}\n "
                f"{self.mascota_relacionada}")
    
    @staticmethod 
    def validar_fecha(fecha):     
        fechav = datetime.datetime.strptime(fecha, "%d-%m-%Y")  # Formato correcto
        if not fechav:
            raise ValueError("La fecha no es correcta")