#Sistema Simple de Gestión para Veterinaria
from MascotaNotFoundError import MascotaNotFoundError
import logging
import json
import Animales, Personas, Historias
import csv
# Listas para almacenar los datos de la clínica veterinaria
nueva_mascota = []  # Almacena todas las mascotas registradas
nueva_consulta = []  # Almacena todas las consultas realizadas
nuevo_duenho = []  # Almacena todos los dueños registrados

# Configurar el logger para registrar las operaciones del programa con un formato de tiempo, nivel de logger y mensaje
logging.basicConfig(filename="clinica_veterinaria.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    encoding="utf-8")


def menu():
    """
    Función principal que muestra el menú de la clínica veterinaria y gestiona las diferentes opciones:
    1. Registro de nuevas mascotas
    2. Registro de consultas veterinarias
    3. Listado de mascotas registradas
    4. Visualización del historial médico de una mascota
    5. Salir del sistema
    """
    while True:
        cargar_mascota_csv()
        cargar_duenho_csv()
        cargar_consultas_json()
        print("=" * 60)
        print("=" * 60)
        print('Menu Principal:\n\n'
              '1. Registrar una mascota.\n'
              '2. Registrar una consulta.\n'
              '3. Listar mascotas.\n'
              '4. Ver historial de consultas de una mascota.\n'
              '5. Salir.\n')
        print("-" * 60)
        opcion = int(input('Seleccione una opcion: '))

        # Opción 1: Registro de nueva mascota y su dueño
        if opcion == 1:
            nombre_mascota = str(input('ingrese el nombre de la mascota: ')).lower().strip().capitalize()
            nombre_duenho = str(input('ingrese el nombre del dueño de la mascota: ')).lower().strip().capitalize()
            if validar_mascota_duenho(nombre_mascota, nombre_duenho):
                guardar_mascota_duenho(nombre_mascota, nombre_duenho)
                print(f"Felicidades! {nombre_mascota} fue añadido con exito\n")
                logging.info(f"la mascota {nombre_mascota} fue registrada")

            else:
                return print("la mascota ya esta registrada"), menu()

        # Opción 2: Registro de nueva consulta veterinaria
        elif opcion == 2:
            while True:
                mascota_relacionada = input(
                    "Ingrese el nombre de la mascota (o escriba 'salir' para cancelar): ").strip().capitalize()
                if mascota_relacionada.lower() == "salir":
                    print("Cancelando el registro de la consulta.")
                    break

                try:
                    if not buscar_mascota(mascota_relacionada):
                        logging.warning(f"la mascota {mascota_relacionada} no existe")
                        raise MascotaNotFoundError(f"No se encontró la mascota '{mascota_relacionada}'.")

                    fecha_consulta = input("Ingrese la fecha de la consulta: ").strip().capitalize()
                    motivo = input("Ingrese el motivo de la consulta: ").strip().capitalize()
                    diagnostico = input("Ingrese el diagnóstico: ").strip().capitalize()

                    consulta = Historias.Consulta(fecha_consulta, motivo, diagnostico, mascota_relacionada)
                    nueva_consulta.append(consulta)
                    logging.info(f"la consulta {consulta} fue registrada")
                    print("✅ Consulta registrada exitosamente.")
                    break


                except MascotaNotFoundError as e:
                    print("Error personalizado:", e)
                    logging.error(f"la mascota {mascota_relacionada} no existe")
                except Exception as e:
                    print("Error:", e)
        # Opción 3: Mostrar listado de mascotas y dueños
        elif opcion == 3:
            listar_mascota()
            listar_duenho()

        # Opción 4: Mostrar historial de consultas de una mascota
        elif opcion == 4:
            nombre_mascota = str(input('ingrese el nombre de la mascota: ')).lower().strip().capitalize()
            if buscar_mascota(nombre_mascota):
                for consulta in nueva_consulta:
                    print("Historial de consultas de la mascota: \n", nombre_mascota)
                    print("Fecha: ", consulta.fecha)
                    print("Motivo de la consulta", consulta.motivo)
                    print("Diagnostico de la mascota", consulta.diagnostico)
            else:
                logging.warning(f"la mascota {nombre_mascota} no existe")
                print("No hay consultas asociadas a la mascota", nombre_mascota)

        # Opción 5: Salir del sistema
        elif opcion == 5:
            logging.info("se ha cerrado el programa")
            exit()

            
        else:
            print("Opcion no valida")


def cargar_mascota_csv():
    with open("mascotas.csv","r") as filecsv:
        datos_mascota=csv.reader(filecsv,delimiter=",")
        
        for fila in datos_mascota:
            nombre, especie, raza, edad = fila
            print(f"{nombre},{especie},{raza},{edad}")
def cargar_duenho_csv():
    with open("duenhos.csv","r") as filecsv:
        datos_duenho=csv.reader(filecsv,delimiter=",")
        
        for fila in datos_duenho:
            nombre, telefono, direccion = fila
            print(f"{nombre},{telefono},{direccion}")
def cargar_consultas_json():
    with open("duenhos.csv","r") as filecsv:
        datos_duenho=csv.reader(filecsv,delimiter=",")
        
        for fila in datos_duenho:
            nombre, telefono, direccion = fila
            print(f"{nombre},{telefono},{direccion}")

def guardar_mascota_duenho(nombre_mascota, nombre_duenho):
    """
    Registra una nueva mascota y su dueño en el sistema.
    Solicita y almacena información detallada de ambos.

    Args:
        nombre_mascota (str): Nombre de la mascota a registrar
        nombre_duenho (str): Nombre del dueño de la mascota

    Returns:
        tuple: Objetos mascota y dueño creados
    """
    especie = str(input('ingrese la especie de la mascota: ')).lower().strip().capitalize()
    raza = str(input('ingrese la raza de la mascota: ')).lower().strip().capitalize()
    while True:
        try:
            edad = int(input('ingrese la edad de la mascota: '))
            if edad <= 0:
                raise ValueError("Ingrese valores númericos positivos.")
            break  # Salir del bucle si todo está bien
        except ValueError as e:
            logging.info("el dato ingresado no es numérico")
            print(f"Error: {e}. Inténtelo de nuevo.")
        except Exception as er:
            logging.info(f"error de la aplicación: {er}")

    print("Ahora ingrese los datos del dueño:")
    while True:
        try:
            telefono = int(input('Ingrese el teléfono de la persona: '))
            if telefono <= 0:
                logging.info("Valor numérico no positivo")
                raise ValueError("Ingrese valores númericos positivos.")
            break  # Salir del bucle si todo está bien
        except ValueError as e:
            logging.error("el dato ingresado no es númerico")
            print(f"Error: {e}. Inténtelo de nuevo.")
        except Exception as err:
            logging.error(f"error de la aplicación: {err}")

    direccion = str(input("ingrese la dirección del dueño: ")).lower().strip().capitalize()

    # Crear y guardar los objetos
    mascota = Animales.Mascota(nombre_mascota, especie, raza, edad, nombre_duenho)
    with open("mascotas.csv",mode="a") as file:
        
        mascotacsv=csv.writer(file, delimiter=",")
        mascotacsv.writerow([nombre_mascota,especie,raza,edad])
    nueva_mascota.append(mascota)
    duenho = Personas.Duenho(nombre_duenho, telefono, direccion)
    with open("duenhos.csv",mode="a") as file_duenho:
        
        duenhocsv=csv.writer(file_duenho, delimiter=",")
        duenhocsv.writerow([nombre_duenho,telefono,direccion])
    nuevo_duenho.append(duenho)
    return mascota, duenho, mascotacsv, duenhocsv


def buscar_mascota(mascota_relacionada):
    """
    Verifica si una mascota está registrada en el sistema.

    Args:
        mascota_relacionada (str): Nombre de la mascota a buscar

    Returns:
        bool: True si la mascota existe, False en caso contrario
    """
    for mascota in nueva_mascota:
        if mascota.nombre_mascota == mascota_relacionada:
            return True
    return False


def validar_mascota_duenho(nombre_mascota, nombre_duenho):
    """
    Verifica que no exista una combinación duplicada de mascota y dueño.

    Args:
        nombre_mascota (str): Nombre de la mascota
        nombre_duenho (str): Nombre del dueño

    Returns:
        bool: True si la combinación es única, False si ya existe
    """
    for mascota in nueva_mascota:
        if mascota.nombre_mascota == nombre_mascota and mascota.duenho == nombre_duenho:
            return False
    return True


def listar_mascota():
    """
    Muestra en pantalla todas las mascotas registradas en el sistema
    con sus respectivos detalles.

    Returns:
        bool: False si no hay mascotas registradas
    """
    if not nueva_mascota:
        logging.warning("no hay mascotas registradas")
        print("No hay mascotas registradas en el sistema")
        return False
    # el metodo enumarate() devuelve una tupla con el indice y el valor de la lista comenzando a contar en 1
    for i, mascota in enumerate(nueva_mascota, 1):
        print("=" * 60)
        print(f"Mascota {i}")
        print("=" * 60)
        print("Nombre de la mascota: ", mascota.nombre_mascota)
        print("Especie de la mascota: ", mascota.especie)
        print("Raza de la mascota: ", mascota.raza)
        print("Edad de la mascota: ", mascota.edad)
        print("Dueño de la mascota: ", mascota.duenho)
    return False


def listar_duenho():
    """
    Muestra en pantalla todos los dueños registrados en el sistema
    con sus respectivos detalles.

    Returns:
        bool: False si no hay dueños registrados
    """
    if not nuevo_duenho:
        logging.warning("no hay dueños registrados")
        print("No hay dueños registrados en el sistema")
        return False
    """
               enumerate(nuevo_duenho, 1) hace dos cosas:
               1. Itera sobre la lista 'nuevo_duenho'
               2. Genera índices empezando desde 1 (no desde 0)
               - i: será el número de dueño (1, 2, 3...)
               - duenho: será el objeto Duenho actual en la iteración
               """
    for i, duenho in enumerate(nuevo_duenho, 1):
        print("*" * 60)
        print(f"Dueño {i}")
        print("*" * 60)
        print("Nombre del dueño: ", duenho.nombre_duenho)
        print("Telefono: ", duenho.telefono)
        print("Direccion: ", duenho.direccion)
    return False


# Iniciar el programa y registrar el log
logging.info("se ha iniciado el programa")
menu()