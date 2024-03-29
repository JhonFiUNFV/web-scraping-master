"""
OBJETIVO:
    - Extraer los titulares y el resumen de las noticias en la pagina principal de deportes de EL UNIVERSO.
    - Contrastar el uso de Beautiful Soup y Scrapy para parsear el arbol HTML.
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 21 abril 2021
"""

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess

# ABSTRACCION DE DATOS A EXTRAER - DETERMINA LOS DATOS QUE TENGO QUE LLENAR Y QUE ESTARAN EN EL ARCHIVO GENERADO
class Noticia(Item):
    id = Field()
    titular = Field()
    descripcion = Field()


# CLASE CORE - SPIDER
class ElUniversoSpider(Spider):
    name = "MiSegundoSpider"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        # 'FEED_EXPORT_FIELDS': ['id', 'descripcion', 'titular'], # Como ordenar las columnas en el CSV?
        # 'CONCURRENT_REQUESTS': 1 # numero de requerimientos concurrentes
        #'FEED_EXPORT_ENCODING': 'utf-8'
    }
    start_urls = ['https://www.eluniverso.com/deportes']

    def parse(self, response):
         soup = BeautifulSoup(response.body)
         contenedor_noticias=soup.find_all(class_="feed | divide-y relative")
         id = 0

         for contenedor in contenedor_noticias:
           noticias = contenedor.find_all(class_='relative', recursive = False)
           for noticia in noticias:
             item = ItemLoader(Noticia(), response.body)
             titular = noticia.find('h2').text.replace('\n', '').replace('\r', '')
             descripcion = noticia.find('p')
             if (descripcion):
               item.add_value('descripcion', descripcion.text.replace('\n', '').replace('\r', ''))
             else:
               item.add_value('descripcion', 'N/A')
             item.add_value('titular', titular)
             item.add_value('id', id)
             id += 1
             yield item.load_item()
