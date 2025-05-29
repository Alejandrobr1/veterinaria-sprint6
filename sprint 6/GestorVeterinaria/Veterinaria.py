#Sistema Simple de Gestión para Veterinaria

from GestorVeterinaria.MascotaNotFoundError import MascotaNotFoundError
import logging
import json
import Animales, Personas, Historias
import csv
# Listas para almacenar los datos de la clínica veterinaria
nueva_mascota = []  # Almacena todas las mascotas registradas


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


        print("=" * 60)
        print("=" * 60)
        print('Menu Principal:\n\n'
              '1. Registrar una mascota.\n'
              '2. Registrar una consulta.\n'
              '3. Listar mascotas.\n'
              '4. Ver historial de consultas de una mascota.\n'
              '5. Salir.\n')
        print("-" * 60)
        try:
            opcion = int(input('Seleccione una opcion: '))
            if opcion not in [1, 2, 3, 4, 5]:
                raise ValueError("Opción no válida")
        except ValueError as e:
            logging.error(f"Ingreso de opción no válida en sistema {e}")
            print("Por favor, ingrese un número válido entre 1 y 5")
            return menu()

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
                # Inicializar variable para rastrear si se encontró la mascota
                mascota_encontrada = False

                # Solicitar el nombre de la mascota y formatear la entrada
                mascota_relacionada = input("Ingrese el nombre de la mascota (o escriba 'salir' para cancelar): ").strip().capitalize()

                # Verificar si el usuario desea salir del registro de consulta
                if mascota_relacionada == "Salir":
                    print("Cancelando el registro de la consulta.")
                    break

                # Abrir y leer el archivo CSV de mascotas
                with open("mascotas.csv", "r") as filecsv:
                    datos_mascota = csv.reader(filecsv, delimiter=",")

                    # Buscar la mascota en el archivo CSV
                    for mascota in datos_mascota:
                        # Verificar si la mascota existe y coincide con el nombre buscado
                        if mascota and mascota[0] == mascota_relacionada:  # mascota[0] es el nombre de la mascota
                            mascota_encontrada = True
                            try:
                                # Recopilar datos de la consulta
                                fecha_consulta = input("Ingrese la fecha de la consulta: ").strip().capitalize()
                                motivo = input("Ingrese el motivo de la consulta: ").strip().capitalize()
                                diagnostico = input("Ingrese el diagnóstico: ").strip().capitalize()

                                # Crear objeto consulta con los datos recopilados
                                consulta = Historias.Consulta(fecha_consulta, motivo, diagnostico, mascota_relacionada)

                                # Cargar consultas existentes del archivo JSON
                                datos_consultas = cargar_consultas_existentes()

                                # Preparar nueva consulta en formato JSON
                                nueva_consulta_json = {
                                    "Fecha de la consulta": fecha_consulta,
                                    "Motivo": motivo,
                                    "Diagnostico": diagnostico,
                                    "Mascota": mascota_relacionada
                                }

                                # Verificar y crear la lista de consultas si no existe
                                if "consultas" not in datos_consultas:
                                    datos_consultas["consultas"] = []

                                # Agregar la nueva consulta a la lista existente
                                datos_consultas["consultas"].append(nueva_consulta_json)

                                # Guardar la consulta actualizada en el archivo JSON
                                with open("consultas.json", "w") as filejson:
                                    json.dump(datos_consultas, filejson, indent=4)

                                # Registrar la operación en el log y mostrar mensaje de éxito
                                logging.info(f"la consulta {consulta} fue registrada")
                                print("Consulta registrada exitosamente.")

                                # Volver al menú principal después de registrar la consulta
                                menu()
                                 # Asegura que se salga completamente de la función

                            except Exception as e:
                                # Manejar cualquier error durante el proceso
                                print("Error:", e)
                                logging.error(f"Error al registrar consulta: {e}")
                                menu()
                                  # Volver al menú principal en caso de error

                # Si no se encontró la mascota, mostrar mensaje de error
                if not mascota_encontrada:
                    logging.warning(f"Intento de registrar consulta para mascota inexistente: {mascota_relacionada}")
                    raise MascotaNotFoundError(f"Mascota {mascota_relacionada} no encontrada")

        # Opción 3: Mostrar listado de mascotas y dueños
        elif opcion == 3:

            print("-"*60)
            print("Datos de mascotas")
            print("-"*60)
            cargar_mascota_csv()
            print("-"*60)
            print("Datos del dueño")
            print("-"*60)
            cargar_duenho_csv()
        # Opción 4: Mostrar historial de consultas de una mascota
        elif opcion == 4:
            nombre_mascota = str(input('ingrese el nombre de la mascota: ')).lower().strip().capitalize()
            if buscar_mascota(nombre_mascota):
                cargar_consultas_json(nombre_mascota)
            else:
                logging.warning(f"la mascota {nombre_mascota} no existe")
                print("No hay consultas asociadas a la mascota", nombre_mascota)

        # Opción 5: Salir del sistema
        elif opcion == 5:
            logging.info("se ha cerrado el programa")
            exit()

            
        else:
            print("Opcion no valida")

def cargar_consultas_existentes():
    """
     Carga las consultas existentes desde el archivo JSON.
     Si el archivo no existe, crea una estructura de datos vacía.

     Returns:
         dict: Diccionario con todas las consultas existentes o un diccionario
               vacío con la clave 'consultas' si el archivo no existe.

     Estructura del diccionario retornado:
     {
         "consultas": [
             {
                 "Fecha de la consulta": str,
                 "Motivo": str,
                 "Diagnostico": str,
                 "Mascota": str
             },
             ...
         ]
     }
     """

    try:
        # Intentar abrir y cargar el archivo JSON de consultas
        with open("consultas.json", "r") as filejson:
            return json.load(filejson)
    except FileNotFoundError:
        # Si el archivo no existe, retornar una estructura vacía
        return {"consultas": []}

def cargar_mascota_csv():
    """
        Lee y muestra todas las mascotas registradas en el archivo CSV.
        Cada mascota se muestra con su información completa en formato CSV.

        Formato de salida por mascota:
        nombre,especie,raza,edad,dueño

        Manejo de errores:
        - Si el archivo no existe, muestra un mensaje de error
        - Si una fila está vacía, se omite
        - Registra errores en el log del sistema

        Returns:
            None: La función solo imprime la información, no retorna valores
        """

    try:
        # Abrir y leer el archivo CSV de mascotas
        with open("mascotas.csv", "r") as filecsv:
            datos_mascota = csv.reader(filecsv, delimiter=",")
            # Iterar sobre cada fila del archivo
            for fila in datos_mascota:
                # Verificar que la fila contenga datos

                if fila:  # Verifica que la fila no esté vacía
                    # Desempaquetar los datos de la mascota
                    nombre, especie, raza, edad, duenho = fila
                    # Mostrar la información en formato CSV
                    print(f"{nombre},{especie},{raza},{edad},{duenho}")
    except FileNotFoundError:
        print("El archivo mascotas.csv no existe.")
        logging.error("El archivo mascotas.csv no existe.")


def cargar_duenho_csv():
    try:
        with open("duenhos.csv","r") as filecsv:
            datos_duenho=csv.reader(filecsv,delimiter=",")

            for fila in datos_duenho:
                if fila:
                    nombre, telefono, direccion = fila
                    print(f"{nombre},{telefono},{direccion}")
    except FileNotFoundError:
        print("El archivo duenhos.csv no existe.")
        logging.error("El archivo duenhos.csv no existe.")
def cargar_consultas_json(nombre_mascota):
    with open("consultas.json", "r") as filejson:
        datos = json.load(filejson)

        """Se crea una nueva lista para almacenar las mascotas consultadas consulta_mascota=[]
        itera el ciclo for y si el nombre de la mascota encuentra una coincidencia en el valor de la llave 
        consulta["Mascota"] entonces va a tomar esa consulta especifica con sus demas datos de llave:valor 
        y la va a añadir a la lista consultas_mascota"""
        consultas_mascota = [consulta for consulta in datos["consultas"]
                             if consulta["Mascota"] == nombre_mascota]
        """si la consulta de nombre mascota existe en el archivo json, me va a devolver los demas datos de esa consulta
        devuelve fecha motivo y diagnostico de la mascota buscada y si no, imprime un mensaje indicando que no hay
        consultas de mascotas con el nombre buscado registradas"""
        if consultas_mascota:
            print(f"\nConsultas encontradas para {nombre_mascota}:")
            for consulta in consultas_mascota:
                print("-"*60)
                print(f"Fecha: {consulta['Fecha de la consulta']}")
                print(f"Motivo: {consulta['Motivo']}")
                print(f"Diagnóstico: {consulta['Diagnostico']}")
            return consultas_mascota
        else:
            print(f"No se encontraron consultas para la mascota {nombre_mascota}")
            return None


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
        mascotacsv.writerow([nombre_mascota,especie,raza,edad,nombre_duenho])
    nueva_mascota.append(mascota)
    duenho = Personas.Duenho(nombre_duenho, telefono, direccion)
    with open("duenhos.csv",mode="a") as file_duenho:
        
        duenhocsv=csv.writer(file_duenho, delimiter=",")
        duenhocsv.writerow([nombre_duenho,telefono,direccion])
    return mascota, duenho, mascotacsv, duenhocsv


def buscar_mascota(mascota_relacionada):
    """
    Verifica si una mascota está registrada en el sistema.

    Args:
        mascota_relacionada (str): Nombre de la mascota a buscar

    Returns:
        bool: True si la mascota existe, False en caso contrario
    """
    with open("consultas.json","r") as file:
        datos=json.load(file)

        for consulta in datos["consultas"]:
            if consulta["Mascota"] == mascota_relacionada:
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



# Iniciar el programa y registrar el log
logging.info("se ha iniciado el programa")
menu()