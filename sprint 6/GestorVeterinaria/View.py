from Controller import *
from Models import Mascota,Duenho,Consulta
import logging

logging.basicConfig(filename='clinica_veterinaria.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

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
            if validar_existencia_mascota_duenho(nombre_mascota, nombre_duenho):
                print("La mascota ya está registrada con ese dueño.")
                logging.warning(f"Intento de registrar mascota ya existente: {nombre_mascota} para el dueño {nombre_duenho}")
                menu()
            especie = str(input('ingrese la especie de la mascota: ')).lower().strip().capitalize()
            raza = str(input('ingrese la raza de la mascota: ')).lower().strip().capitalize()
            while True:
                try:
                    edad = input('Ingrese la edad de la mascota: ')
                    Mascota.validar_edad(edad)
                    edad = int(edad)
                    break
                except (ValueError, TypeError):
                    print("El valor debe ser numérico y positivo.")
                    logging.error("El valor ingresado no es numérico o positivo: ", edad)
            print("Ahora ingrese los datos del dueño:")
            while True:
                try:
                    telefono = input('Ingrese el teléfono de la persona: ')
                    Duenho.validar_telefono(telefono)
                    break
                except (ValueError,TypeError):
                    print("El valor debe ser numérico y positivo.")
                    logging.error("El valor ingresado no es numérico o positivo: ", telefono)
            direccion = str(input("ingrese la dirección del dueño: ")).lower().strip().capitalize()
    
            if registrar_mascota_duenho(nombre_mascota, especie, raza, edad, nombre_duenho, telefono, direccion):
                    print(f"Felicidades! {nombre_mascota} fue añadido con exito\n")
                    logging.info(f"la mascota {nombre_mascota} fue registrada")
            else:
                return print("la mascota ya esta registrada"), menu()

        # Opción 2: Registro de nueva consulta veterinaria
        elif opcion == 2:         
            mascota_relacionada = input("Ingrese el nombre de la mascota (o escriba 'S' para cancelar): ").strip().capitalize()   
            if mascota_relacionada == "S": # Verificar si el usuario desea salir del registro de consulta
                print("Cancelando el registro de la consulta.")
                break
            if not validar_existencia_mascota_consulta(mascota_relacionada):
                print(f"La mascota {mascota_relacionada} no está registrada, registrela!.")
                menu()         
            while True:
                try:
                    fecha = input("Ingrese la fecha de la consulta (DD-MM-AAAA): ").strip()
                    Consulta.validar_fecha(fecha)  # Validar formato de fecha
                    break
                except (ValueError,TypeError) as e:
                    logging.error(f"Fecha ingresada no válida: {e}")
                    print("Fecha no válida. Por favor, ingrese una fecha en formato DD-MM-AAAA.")
                    continue
            motivo = input("Ingrese el motivo de la consulta: ").strip()
            diagnostico = input("Ingrese el diagnóstico: ").strip()
            if registrar_consulta(fecha, motivo, diagnostico, mascota_relacionada):
                print(f"La consulta para {mascota_relacionada} ha sido registrada exitosamente.")
                logging.info(f"Consulta registrada para la mascota {mascota_relacionada} con fecha {fecha}")
            else:
                print("Error al registrar la consulta. Verifique los datos ingresados.")
                logging.error(f"Error al registrar la consulta para la mascota {mascota_relacionada}")
                
        # Opción 3: Mostrar listado de mascotas y dueños
        elif opcion == 3:
            print("-"*60)
            print("Datos de las mascotas")
            print("-"*60)
            listar_mascotas()
            print("\n")
            print("-"*60)
            print("Datos de los dueño")
            print("-"*60)
            listar_duenhos()
        # Opción 4: Mostrar historial de consultas de una mascota
        elif opcion == 4:
            
            nombre_mascota = str(input('ingrese el nombre de la mascota: ')).lower().strip().capitalize()
            if buscar_mascota(nombre_mascota):
                if not cargar_consultas_json(nombre_mascota):
                    logging.warning(f"la mascota {nombre_mascota} no tiene consultas registradas")
                    print("No hay consultas asociadas a la mascota", nombre_mascota)
            else:
            
                logging.warning(f"la mascota {nombre_mascota} no existe")
                print("No hay consultas asociadas a la mascota", nombre_mascota)
        # Opción 5: Salir del sistema
        elif opcion == 5:
            logging.info("se ha cerrado el programa")
            exit()

            
        else:
            print("Opcion no valida")
            logging.error("Opción no válida ingresada por el usuario")

if __name__ == "__main__":
    menu()

