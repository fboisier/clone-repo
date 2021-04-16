import time
import git
from git import RemoteProgress
import csv
import sys
import os
import logging
import shutil

# Script para poder descargar todos los repositorios de un ejercicio de alumnos. 
# toma el archivo repositorios que debe tener como minimo 3 columnas, nombre, apellido y github
# creará una carpeta con el nombre del ejercicio. 
# pedirá nombre del ejercicio que fue dado a los alumnos para descargar.
# si no se encuentra alguna carpeta será dejado en un archivo log de ejecución. 
# requisitos instalar GitPython:  pip install GitPython
formatter = logging.Formatter('%(asctime)s - %(message)s')


def setup_logger(name, log_file, level=logging.INFO):

    handler = logging.FileHandler(log_file,encoding='utf-8')        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

logger = setup_logger('resultado', 'resultado.log')
faltantes = setup_logger('faltantes', 'faltantes.log')

def log_p(mensaje):
    print(mensaje)
    logger.info(mensaje)

def log_f(mensaje):
    faltantes.info(mensaje)

def eliminarRuta(ruta):
    salida = ""
    # Detectar Sistema Operativo
    if sys.platform == "win32":
        salida = "rmdir /s /q " + ruta
    else:
        salida = "rm -rf " + ruta
    return salida

log_p("Iniciando Nuevo Proceso de Busqueda de REPOSITORIOS")

class CloneProgress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        if message:
            print(message)

# trabajo = input("Ingresar trabajo a revisar: ")
trabajo = "comunidad-sostenible"
log_p("Abriendo archivo repositorios.csv")
archivo = open("repositorios.csv")
carpetaDescarga = "repositorio_" + trabajo 

log_p("La carpeta de trabajo es: " + carpetaDescarga)

# Creo la estructura de carpetas
if os.path.exists(carpetaDescarga):
    log_p("Eliminando Carpeta " + carpetaDescarga + " para uso desde 0.")
    print(eliminarRuta(carpetaDescarga))
    os.system(eliminarRuta(carpetaDescarga))
os.makedirs(carpetaDescarga)

log_p("*"*10 + "INICIO CREACION DE CARPETAS Y CLONACION" + "*"*10)

reader = csv.DictReader(archivo,delimiter=';')
eliminar = []
for linea in reader:
    # 'nombre' 'apellido' 'github' 
    repo = linea['github'].strip()
    alumno = f"{linea['nombre'].strip()} {linea['apellido'].strip()}".replace(" ", "_")
    carpetaLocal = carpetaDescarga + "/" + alumno
    
    if not os.path.exists(carpetaLocal):
        os.makedirs(carpetaLocal)    
    
    try:
        git.Repo.clone_from(f'{repo}/{trabajo}', carpetaLocal, progress=CloneProgress())
        log_p("Exito en Clonación de " + alumno)
    except:
        log_p("Alumno no sube trabajo: " + alumno)
        log_f(alumno)
        # eliminar carpeta si no tiene datos.
        eliminar.append(carpetaLocal)

log_p("Eliminando directorios sin datos.")
counter = 0
for delete in eliminar:
    if os.path.exists(delete):
        
        try:
            shutil.rmtree(delete)
            counter += 1
        except:
            None

log_p("-"*10 + " ALUMNOS SIN ENTREGAR: " + str(counter) + " " + "-"*10)
log_p("*"*35)
log_p("*"*10 + "FIN DEL PROCESO" + "*"*10)
log_p("*"*35)