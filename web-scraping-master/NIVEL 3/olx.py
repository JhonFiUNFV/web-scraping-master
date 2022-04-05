"""
OBJETIVO:
    - Extraer el precio y el titulo de los anuncios en la pagina de OLX autos.
    - Aprender a realizar extracciones que requieran una accion de click para cargar datos.
    - Introducirnos a la logica de Selenium
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 23 NOVIEMBRE 2020
"""

#####
### ATENCION: OLX necesita que le demos permisos de geolocalizacion al navegador de selenium para que nos muestre los datos
### Esto lo haremos una unica vez en la primer corrida del programa. Este problema es mas comun en usuarios de MAC
#####
import random
from time import sleep
from selenium import webdriver # pip install selenium

# Instancio el driver de selenium que va a controlar el navegador
# A partir de este objeto voy a realizar el web scraping e interacciones
from selenium.webdriver.common.by import By

driver = webdriver.Chrome('./chromedriver') # REMPLAZA AQUI EL NOMBRE DE TU CHROME DRIVER
# Voy a la pagina que requiero
driver.get('https://www.olx.com.pe/items/q-videojuegos')


boton = driver.find_element(By.XPATH, '//button[@data-aut-id="btnLoadMore"]')

for i in range(3):
    try:
        boton.click()
        sleep(random.uniform(8.0, 10.0))
        boton = driver.find_element(By.XPATH, '//button[@data-aut-id="btnLoadMore"]')
    except:
        break
telefonos = driver.find_elements(By.XPATH, '//li[@data-aut-id="itemBox"]')
for telefono in telefonos:
    descripcion= telefono.find_element_by_xpath('.//span[@data-aut-id="itemTitle"]').text
    print(descripcion)
    precio = telefono.find_element_by_xpath('.//span[@data-aut-id="itemPrice"]').text
    print(precio)
