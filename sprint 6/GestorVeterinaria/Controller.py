import csv
import os
import json
import Models
import logging

def crear_archivo_mascotas():
    """
    Crea un archivo CSV para almacenar la información de las mascotas.
    Si el archivo ya existe, no hace nada.
    """
    if not os.path.exists("mascotas.csv"):
        with open("mascotas.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Nombre Mascota", "Especie", "Raza", "Edad", "Dueño"])  # Encabezados del CSV

def crear_archivo_duenhos():
    """
    Crea un archivo CSV para almacenar la información de los dueños de mascotas.
    Si el archivo ya existe, no hace nada.
    """
    if not os.path.exists("duenhos.csv"):
        with open("duenhos.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Nombre Dueño", "Teléfono", "Dirección"])  # Encabezados del CSV

def crear_archivo_consultas():
    """
    Crea un archivo JSON para almacenar la información de las consultas veterinarias.
    Si el archivo ya existe, no hace nada.
    """
    if not os.path.exists("consultas.json") or os.path.getsize("consultas.json") == 0:
        with open("consultas.json", "w") as file:
            json.dump({"consultas": []}, file, indent=4)  # Crea un archivo JSON vacío

def validar_existencia_mascota_duenho(nombre_mascota,nombre_duenho):
    """
    Verifica si una mascota ya está registrada con un dueño específico.
    """
    crear_archivo_mascotas()  # Asegura que el archivo de mascotas exista
    crear_archivo_duenhos()  # Asegura que el archivo de dueños exista
    with open("mascotas.csv", "r") as file:
        filas = csv.reader(file,delimiter=',') # Convertir el lector a una lista para poder iterar
        for mascota in filas:
            if mascota[0] == nombre_mascota and mascota[4]== nombre_duenho:
                return True
        
    return False

def registrar_mascota_duenho(*args):
    mascota=Models.Mascota(nombre_mascota=args[0], especie=args[1], raza=args[2], edad=args[3], duenho=args[4])
    duenho=Models.Duenho(nombre_duenho=args[4], telefono=args[5], direccion=args[6])
    with open("mascotas.csv", "a", newline='') as filemascotas:
        writer = csv.writer(filemascotas)
        writer.writerow([mascota.nombre_mascota, mascota.especie, mascota.raza, mascota.edad, duenho.nombre_duenho])
    with open("duenhos.csv", "a", newline='') as fileduenhos:
        writer = csv.writer(fileduenhos)
        writer.writerow([duenho.nombre_duenho, duenho.telefono, duenho.direccion])
    return mascota, duenho

def validar_existencia_mascota_consulta(mascota_relacionada):
    """
    Verifica si una mascota está registrada en el sistema.
    """
    crear_archivo_mascotas()  # Asegura que el archivo de mascotas exista
    with open("mascotas.csv", "r") as file:
        filas = csv.reader(file)
        for mascota in filas:
            if mascota[0] == mascota_relacionada:
                return True
    return False

def registrar_consulta(fecha, motivo, diagnostico, mascota_relacionada):

    crear_archivo_consultas()  # Asegura que el archivo de consultas exista
    consulta = Models.Consulta(fecha, motivo, diagnostico, mascota_relacionada)
    with open("consultas.json", "r") as file:
        consultas = json.load(file)
        consultas["consultas"].append(consulta.__dict__)  # Agrega la consulta al diccionario de consultas
        
      # Agrega la consulta a la lista de consultas
    with open("consultas.json", "w") as file:
        json.dump(consultas, file, indent=4)  # Guarda la consulta en formato JSON

    return consulta

def listar_mascotas():
    """
    Carga y muestra la lista de mascotas registradas en el sistema.
    """
    crear_archivo_mascotas()  # Asegura que el archivo de mascotas exista
    with open("mascotas.csv", "r") as file:
        mascotas = csv.reader(file)
        next(mascotas)  # Salta la cabecera
        for fila in mascotas:
            print(f"Nombre: {fila[0]}, Especie: {fila[1]}, Raza: {fila[2]}, Edad: {fila[3]}, Dueño: {fila[4]}")

def listar_duenhos():
    """
    Carga y muestra la lista de dueños registrados en el sistema.
    """
    crear_archivo_duenhos()  # Asegura que el archivo de dueños exista
    with open("duenhos.csv", "r") as file:
        duenhos = csv.reader(file)
        next(duenhos)  # Salta la cabecera
        for fila in duenhos:
            print(f"Nombre: {fila[0]}, Teléfono: {fila[1]}, Dirección: {fila[2]}")

def buscar_mascota(nombre_mascota):
    """
    Busca una mascota por su nombre en el archivo de mascotas.
    """
    crear_archivo_mascotas()  # Asegura que el archivo de mascotas exista
    with open("mascotas.csv", "r") as file:
        mascotas = csv.reader(file)
        next(mascotas)  # Salta la cabecera
        for fila in mascotas:
            if fila[0] == nombre_mascota:
                return True
    return False

def cargar_consultas_json(nombre_mascota):
    """
    Carga el historial de consultas de una mascota desde el archivo JSON.
    """
    crear_archivo_consultas()  # Asegura que el archivo de consultas exista
    with open('consultas.json', 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)
        consultas = [consulta for consulta in datos["consultas"] if consulta['mascota_relacionada'] == nombre_mascota]
        if not consultas:
            return False
        for consulta in consultas:
            print(f"Fecha: {consulta['fecha']}, Motivo: {consulta['motivo']}, Diagnóstico: {consulta['diagnostico']}")
        return True