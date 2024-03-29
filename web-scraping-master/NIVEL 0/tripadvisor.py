"""
OBJETIVO:
    - Extraer todas las opiniones de los usuarios que dejan reviews en hoteles de Guayaquil en tripadvisor
    - Aprender a realizar extracciones de dos niveles de verticalidad y dos niveles de horizontalidad
    - Aprender a reducir el espectro de busqueda para filtrar URLs en las reglas
    - Evitar obtener URLs repetidas
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 7 DICIEMBRE 2020
"""
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


class Opinion(Item):
    titulo = Field()
    calificacion = Field()
    contenido = Field()
    autor = Field()



class TripAdvisor(CrawlSpider):
    name = 'hotelestripadvisor'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 100
    }

    allowed_domains = ['tripadvisor.com']
    start_urls = ['https://www.tripadvisor.com/Hotels-g316041-Ayacucho_Ayacucho_Region-Hotels.html']

    download_delay = 1

    rules = (
        Rule(  # https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html
            LinkExtractor(  # PAGINACION DE HOTELES (HORIZONTALIDAD DE PRIMER NIVEL)
                allow=r'-oa\d+-'
            ), follow=True),
        # No tiene callback porque aun no voy a extraer datos de aqui. Solamente voy a seguir otras URLs.
        Rule(
            LinkExtractor(  # DETALLE DE HOTELES (VERTICALIDAD DE PRIMER NIVEL)
                allow=r'/Hotel_Review-',
                restrict_xpaths=['//div[@id="taplc_hsx_hotel_list_lite_dusty_filtered_out_hotels_sponsored_0"]']
                # Evita obtener URLs repetidas reduciendo el espectro de busqueda de las URLs a solamente un contenedor especifico dentro de un XPATH
            ), follow=True),
        # No tiene callback porque aun no voy a extraer datos de aqui. Solamente voy a seguir otras URLs.
        Rule(
            LinkExtractor(  # HORIZONTALIDAD DE OPINIONES DE UN HOTEL (HORIZONTALIDAD DE SEGUNDO NIVEL)
                allow=r'-or\d+-'
            ), follow=True),
        # No tiene callback porque aun no voy a extraer datos de aqui. Solamente voy a seguir otras URLs.
        Rule(
            LinkExtractor(  # DETALLE DE PERFIL DE USUARIO (VERTICALIDAD DE SEGUNDO NIVEL)
                allow=r'/Profile/',
                restrict_xpaths=['//div[@data-test-target="reviews-tab"]']
                # Evita obtener URLs repetidas reduciendo el espectro de busqueda de las URLs a solamente un contenedor especifico dentro de un XPATH
            ), follow=True, callback='parse_opinion'),
    # Aqui si voy a utilizar el callback, debido a que en estas paginas es donde yo quiero extraer datos
    )

    # https://www.tripadvisor.com/Profile/daniaquir0la?fid=25838fc7-bedc-4d3b-b2bc-c0d5a72d6736

    def parse_opinion(self, response):
        sel = Selector(response)
        opiniones = sel.xpath('//div[@id="content"]/div/div')
        autor = sel.xpath('//h1/span/text()').get()
        for opinion in opiniones:
            item = ItemLoader(Opinion(), opinion)
            item.add_value('autor', autor)
            item.add_xpath('titulo', './/div[@class="_3IEJ3tAK _2K4zZcBv"]/text()')
            item.add_xpath('contenido', './/q/text()')
            item.add_xpath('calificacion',
                           './/div[contains(@class, "ui_card section")]//a/div/span[contains(@class, "ui_bubble_rating")]/@class',
                           MapCompose(lambda i: i.split('_')[-1]))
            yield item.load_item()


# EJECUCION
# scrapy runspider 4_tripadvisor.py -o tripadvisor_users.csv -t csv