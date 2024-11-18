import json
import os

def cargar_datos_usuario(nombre_usuario):
    """
    Carga los datos del usuario desde el archivo JSON.
    """
    ruta_carpeta = "Data/respuestas"
    nombre_archivo = f"respuestas_{nombre_usuario}.json"
    ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
    try:
        with open(ruta_completa, 'r') as f:
            datos_usuario = json.load(f)
        return datos_usuario
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta_completa}")
        return None

def guardar_respuestas(usuario, respuestas):
    """
    Guarda las respuestas del usuario en un archivo JSON en la ruta especificada.
    """
    ruta_carpeta = "Data/respuestas"  # Define la ruta de la carpeta
    nombre_archivo = f"respuestas_{usuario['nombre']}.json"  # Nombre del archivo
    ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)  # Combina la ruta y el nombre

    # Crear la carpeta si no existe
    os.makedirs(ruta_carpeta, exist_ok=True)

    try:
        with open(ruta_completa, 'w') as f:
            json.dump(respuestas, f, indent=4)
        print(f"Respuestas guardadas en {ruta_completa}")
    except Exception as e:
        print(f"Error al guardar las respuestas: {e}")

def cargar_datos_tests():
    """
    Carga los datos de todos los tests desde los archivos JSON.
    """
    ruta_carpeta = "Data/test"
    datos_tests = {}
    try:
        for nombre_archivo in os.listdir(ruta_carpeta):
            if nombre_archivo.endswith(".json"):
                ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
                with open(ruta_completa, 'r') as f:
                    test = json.load(f)
                    
                    # Adaptar la lógica de seleccionar_preguntas_aleatorias
                    if "mini_ipip_test" in test:
                        preguntas = []
                        for dimension in test["mini_ipip_test"].values():
                            if "questions" in dimension:
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
                        continue  # Saltar al siguiente archivo si la estructura no es reconocida

                    # Almacenar las preguntas en datos_tests
                    nombre_test = nombre_archivo[:-5]
                    datos_tests[nombre_test] = {'preguntas': preguntas}  # Almacenar solo las preguntas

        return datos_tests
    except FileNotFoundError:
        print(f"Error: No se encontró la carpeta {ruta_carpeta}")
        return None
    
def buscar_id_pregunta(pregunta_usuario, datos_tests):
    """
    Busca el ID de la pregunta en los datos de los tests.
    """
    pregunta_usuario = pregunta_usuario.lower()
    for nombre_test, test in datos_tests.items():
        for pregunta in test['preguntas']:
            if pregunta_usuario in pregunta['text'].lower():
                return pregunta['id']
    return None