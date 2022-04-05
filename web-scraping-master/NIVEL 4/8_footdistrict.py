"""
    Objetivo: Extraer las tallas de los zapatos
"""
import requests
import json
from lxml import html # pip install lxml

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
}


url = "https://footdistrict.com/adidas-ultra-boost-ltd-af5836.html"

resp = requests.get(url, headers=headers)
parser = html.fromstring(resp.text)

datos = parser.xpath("//script[contains(text(), 'spConfig')]")
texto_script = datos[0].text_content()
print (texto_script)


ini = texto_script.find('(') + 1 # Obtengo la posicion de mi cadena donde se encuentra el parentesis abierto
fin = texto_script.find(')') # Obtengo la posicion de mi cadena donde se encuentra el parentesis cerrado

objeto = texto_script[ini:fin] # Con las posiciones, puedo cortar la cadena. A esto se le llama slicing, o obtener un substring.

objeto = json.loads(objeto) # Cargo el json a un diccionario

# Sabiendo la estructura del diccionario lo recorro para obtener la informacion que quiero
tallas = objeto["attributes"]["134"]["options"]
for talla in tallas:
  if "No disponible" not in talla["label"]: # filtro las tallas que no estan disponibles
    print (talla["label"]) # Imprimo por pantalla
