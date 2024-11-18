import json
import random


def generar_preguntas_iniciales():
    mini_ipip_test = cargar_preguntas("BigFive")
    eneagrama_test = cargar_preguntas("Eneagrama")
    sds_test = cargar_preguntas("SelfDirectedSearch")
    strong_test = cargar_preguntas("StrongInterestInventory")
    preguntas = []
   
    preguntas.extend(seleccionar_preguntas_aleatorias(mini_ipip_test, 2))
    preguntas.extend(seleccionar_preguntas_aleatorias(eneagrama_test, 2))
    preguntas.extend(seleccionar_preguntas_aleatorias(sds_test, 2))
    preguntas.extend(seleccionar_preguntas_aleatorias(strong_test, 2))

    random.shuffle(preguntas) 
    return preguntas


def cargar_preguntas(nombre_archivo):
    """
    Carga las preguntas de un test desde un archivo JSON.
    """
    try:
        with open(f'Data/test/{nombre_archivo}.json', 'r', encoding='utf-8') as f:  
            test = json.load(f)
            print(test)  # Verificar el contenido del diccionario
        return test
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo Data/test/{nombre_archivo}.json")  
        return None

def seleccionar_preguntas_aleatorias(test, num_preguntas):
    """
    Selecciona preguntas aleatorias de un test.
    """
    if "mini_ipip_test" in test:
        preguntas = []
        for dimension in test["mini_ipip_test"].values():
            if "questions" in dimension:  # Verificar si la clave "questions" existe
                preguntas.extend(dimension["questions"])
    elif "eneagrama_test" in test:
        preguntas = []
        for tipo in test["eneagrama_test"]["types"].values():
            preguntas.extend(tipo["questions"])
    elif "self_directed_search" in test:
        preguntas = []
        for area in test["self_directed_search"].values():
            if isinstance(area, dict) and "questions" in area:
                preguntas.extend(area["questions"])
    elif "strong_interest_inventory" in test:
        preguntas = test["strong_interest_inventory"]["preguntas"]
    else:
        print("Error: Estructura de JSON no reconocida.")
        return []

    if num_preguntas > len(preguntas):
        num_preguntas = len(preguntas)
    return random.sample(preguntas, num_preguntas)

def calcular_puntajes(respuestas, test):
    """
    Calcula los puntajes del test basándose en las respuestas del usuario.
    """
    puntajes = {}
    for dimension, datos in test.items():
        if dimension not in ["escala_respuestas", "instructions", "response_type", "codigos_riasec", "areas_ocupacionales", "tipos"]:  # Ignorar las claves que no son dimensiones
            puntajes[dimension] = 0
            for pregunta in datos["questions"]:
                id_pregunta = pregunta["id"]
                respuesta = respuestas.get(id_pregunta)
                if respuesta:
                    puntaje = int(respuesta)
                    if pregunta.get("inversa", False):
                        puntaje = 6 - puntaje  # Invertir el puntaje si la pregunta es inversa
                    puntajes[dimension] += puntaje * pregunta["peso"]
    return puntajes