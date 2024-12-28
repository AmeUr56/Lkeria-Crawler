# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class AnnounceItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    agence = scrapy.Field()
    location = scrapy.Field()
    kind = scrapy.Field() # Location ou Vente
    area = scrapy.Field()
    pieces = scrapy.Field()
    reference = scrapy.Field()
    phone_numbers = scrapy.Field()
    price = scrapy.Field()

class ExpertItem(scrapy.Item):
    url = scrapy.Field()
    wilaya = scrapy.Field()
    kind = scrapy.Field() # Notaire ou Architect our Geometre ou Promoteur
    title = scrapy.Field()
    fix_number = scrapy.Field()
    phone_number = scrapy.Field()
    addresse = scrapy.Field()
    description = scrapy.Field()
    
class AgenceItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    kind = scrapy.Field() # Imobilier ou Administrateur des biens
    phone_number1 = scrapy.Field()
    phone_number2 = scrapy.Field() 
    phone_number3 = scrapy.Field()
    website = scrapy.Field()
    addresse = scrapy.Field()
    registre = scrapy.Field()
    agrement = scrapy.Field()
    description = scrapy.Field()
    