import scrapy
from ..items import ExpertItem

class ExpertsSpidersSpider(scrapy.Spider):
    name = "experts_spiders"
    allowed_domains = ["www.lkeria.com"]
    start_urls = ["https://www.lkeria.com/Architecte-Algerie.html",
                  "https://www.lkeria.com/Notaire-Algerie.html",
                  "https://www.lkeria.com/Geometre-expert-foncier-Algerie.html",
                  "https://www.lkeria.com/Promoteur-Immobilier-Algerie.html"
                  ]

    def parse(self, response):
        self.logger.info(f"Processing page: {response.url}")
        
        wilayas_url = response.xpath("//div[@class='noo-wrapper']//div[@class='row']//div[@class='col-xs-12 col-md-4']/a/@href").getall()

        # Crawl each Wilaya 
        for url in wilayas_url:
            full_url = "https://www.lkeria.com/" + url.split(".")[0] + "-1.html"
            yield scrapy.Request(full_url,callback=self.parse_wilaya)
            
    def parse_wilaya(self, response):
        self.logger.info(f"Processing Wilaya: {response.url}")
        
        experts = response.xpath("//div[@class='agents grid clearfix']//article[@class='hentry']")
        
        # Crawl each Expert
        for expert in experts:
            url = expert.xpath(".//a/@href").get()
            full_url = "https://www.lkeria.com/" + url
            yield scrapy.Request(full_url,callback=self.parse_expert)
    
        # Crawl Other Pages        
        next_page_url = response.xpath("//ul[@class='pagination list-center']/li[a[@current] or a[contains(@class,'current')]]/following-sibling::li[1]/a/@onclick").get()
        
        if next_page_url:
            next_page_full_url = "https://www.lkeria.com/" + next_page_url.split(",")[1].split("\"")[1]
            self.logger.info(f"Following next page: {next_page_url}")
            yield scrapy.Request(next_page_full_url,callback=self.parse)
        else:
            self.logger.info("No next page found.")
          
    def parse_expert(self, response):
        self.logger.info(f"Processing Expert: {response.url}")
        
        expert_item = ExpertItem()
        
        main = response.xpath("//div[@class='noo-wrapper']//div[@class='noo-content col-xs-12 col-md-8']")
        
        expert_item['url'] = response.url
        
        full_title = main.xpath(".//h1/text()").get().split(" ")
        expert_item['kind'] = full_title[0]
        expert_item['title'] = " ".join(full_title[1:])
        expert_item['wilaya'] = response.xpath("//div[@class='noo-wrapper']//div[@class='block-sidebar find-property']/a/strong/text()").get()

        try: 
            expert_item['fix_number'] = main.xpath(f".//div[@id='tab-infos']//div[i[@class='fa fa-phone']]/text()")[-1].get()
        except:
            expert_item['fix_number'] = None
        try: 
            expert_item['phone_number'] = main.xpath(f".//div[@id='tab-infos']//div[i[@class='fa fa-mobile']]/text()")[-1].get()
        except:
            expert_item['phone_number'] = None

        expert_item['addresse'] = main.xpath(f".//div[@id='tab-infos']//div[i[@class='fa fa-home']]/text()")[-1].get()
        expert_item['description'] = main.xpath(".//div[@id='tab-infos']//div[@class='agent-desc']/p/text()").get()
    
        yield expert_item