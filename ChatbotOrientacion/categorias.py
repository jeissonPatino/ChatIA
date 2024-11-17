import json

def cargar_categorias():
  with open('Data/Categorias.json', 'r') as f:
    categorias = json.load(f)
  return categorias

categorias = cargar_categorias()