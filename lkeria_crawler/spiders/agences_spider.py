import scrapy
from ..items import AgenceItem

class AgencesSpiderSpider(scrapy.Spider):
    name = "agences_spider"
    allowed_domains = ["www.lkeria.com"]
    start_urls = ["https://www.lkeria.com/Agences-Immobilieres-Algerie.html"
                  ,"https://www.lkeria.com/administrateurs-biens-algerie"
                  ]

    def parse(self, response):
        self.logger.info(f"Processing Page: {response.url}")
        
        wilayas_url = response.xpath("//div[@class='noo-content col-xs-12 col-md-8']//div[@class='col-xs-12 col-md-4 text-left']/a/@href").getall()

        for url in wilayas_url:
            full_url = "https://www.lkeria.com/" + url
            yield scrapy.Request(full_url,callback=self.parse_wilaya)
            
    def parse_wilaya(self, response):
        self.logger.info(f"Processing Wilaya: {response.url}")
        
        agences = response.xpath("//div[@class='agents grid clearfix']//article[@class='hentry']")
        
        # Crawl each Agence
        for agence in agences:
            url = agence.xpath(".//a[@class='content-thumb']/@href").get()
            if "immobiliere" in response.url:
                url =  url.split(".")[0] + "-1.html"
                
            full_url = "https://www.lkeria.com/" + url
            yield scrapy.Request(full_url,callback=self.parse_agence)

        # Crawl Other Pages        
        next_page_url = response.xpath("//ul[@class='pagination list-center']/li[a[@current] or a[contains(@class,'current')]]/following-sibling::li[1]/a/@onclick").get()
        
        if next_page_url:
            next_page_full_url = "https://www.lkeria.com/" + next_page_url.split(",")[1].split("\"")[1]
            self.logger.info(f"Following next page: {next_page_url}")
            yield scrapy.Request(next_page_full_url,callback=self.parse)
        else:
            self.logger.info("No next page found.")
            
    def parse_agence(self,response):
        self.logger.info(f"Processing Agence: {response.url}")
        
        agence_item = AgenceItem()
        main = response.xpath("//div[@class='agent-detail']")
        
        agence_item['url'] = response.url
        agence_item['title'] = response.xpath("//article[@class='noo-agent']/h1[@class='content-title']/a/text()").get()
        #agence_item['kind'] = response.xpath("//article[@class='noo-agent']/h1[@class='content-title']/img/following-sibling::text()[1]").get()
        agence_item['kind'] = "Agence Immobilier" if "immobiliere" in response.url else "Administrateurs de biens"
        
        infos = main.xpath(".//div[@class='agent-detail-info']") 
        #detail = lambda info: infos.xpath(f".//div[span[text() = '{info}:']]/text()[2]").get()

        agence_item["phone_number1"] = infos.xpath(".//div[span[text() = 'Mobile 1:']]/text()[2]").get()
        agence_item["phone_number2"] = infos.xpath(".//div[span[text() = 'Mobile 2:']]/text()[2]").get()
        agence_item["phone_number3"] = infos.xpath(".//div[span[text() = 'Mobile 3:']]/text()[2]").get()
        agence_item["website"] = infos.xpath(".//div[span[text() = 'Site web:']]/text()[2]").get()

        agence_item["addresse"] = infos.xpath(".//div[span[text() = 'Adresse:']]/text()[2]").get()
        agence_item["registre"] = infos.xpath(".//div[span[text() = 'Registre:']]/text()[2]").get()
        agence_item["agrement"] = infos.xpath(".//div[span[text() = 'Agrément:']]/text()[2]").get()

        agence_item["description"] = main.xpath("./div[@class='agent-desc']/p/text()").get()

        yield agence_item