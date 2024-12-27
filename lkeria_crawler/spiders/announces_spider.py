import scrapy
from ..items import AnnounceItem

class AnnouncesSpiderSpider(scrapy.Spider):
    name = "announces_spider"
    allowed_domains = ["www.lkeria.com"]
    start_urls = ["https://www.lkeria.com/annonces/immobilier/location-algerie-P1",
                  "https://www.lkeria.com/annonces/immobilier/vente-algerie-P1"]

    def parse(self, response):
        self.logger.info(f"Processing page: {response.url}")
        
        articles = response.xpath(f"//body//form[@id='fResultat_{response.url.split('/')[-1].split('-')[0]}']//div[@class='noo-wrapper']//div[@class='properties-content']/article")        

        # Crawl each Announce
        for article in articles:
            url = "https:" + article.xpath(".//a")[-1].xpath("@href").get()

            yield scrapy.Request(url,callback=self.parse_announce)
        
        # Crawl Other Pages
        
        next_page_url = response.xpath("//ul[@class='pagination list-center']/li[a[contains(@class,'current')]]/following-sibling::li[1]/a/@href").get()

        if next_page_url:
            self.logger.info(f"Following next page: {next_page_url}")
            yield scrapy.Request(next_page_url,callback=self.parse)
        else:
            self.logger.info("No next page found.")
        
    def parse_announce(self, response):
        self.logger.info(f"Processing Announce: {response.url}")
        
        annonce_item = AnnounceItem()

        main = response.xpath("//div[@class='noo-content col-xs-12 col-md-8']")
        annonce_item["url"] = response.url
        annonce_item["kind"] = "Location" if "Location" in response.url else "Vente"
        annonce_item['title'] = main.xpath(".//h1[@class='titre']/span/text()").get()
        annonce_item['price'] = main.xpath(".//span[@class='hidden-md prix-resume']/text()").get()
        annonce_item['area'] = main.xpath(".//ul[@class='resume']/li[1]/text()").get()
        annonce_item['pieces'] = main.xpath(".//ul[@class='resume']/li[2]/text()").get()
        try:
            annonce_item['location'] = main.xpath(".//div[@class='row']/div[@class='g-row gauche col-sm-12 col-md-6']")[1].xpath(".//text()").get()
        except:
            annonce_item['location'] = main.xpath(".//div[@class='row']/div[@class='g-row gauche col-sm-12 col-md-6']").xpath(".//text()").get()

        try:
            annonce_item['reference'] = main.xpath(".//div[@class='row']/div[@class='g-row droit col-sm-12 col-md-6']")[-1].xpath(".//text()").get()
        except:
            annonce_item['reference'] = main.xpath(".//div[@class='row']/div[@class='g-row droit col-sm-12 col-md-6']").xpath(".//text()").get()
            
        main_description = main.xpath(".//section[@itemprop='description']")
        annonce_item['description'] = "\n".join(main_description.xpath(".//p/text()").getall())
        try:
            annonce_item["phone_numbers"] = main_description.xpath("text()")[-1].get()
        except:
            annonce_item["phone_numbers"] = main_description.xpath("text()").get()
            
        annonce_item['agence'] = main.xpath(".//section[@id='agence']//h3/span[@itemprop='name']/text()").get()
        
        yield annonce_item