import re
import scrapy
from scrapy.crawler import CrawlerProcess


class PlantInfoSpider(scrapy.Spider):
    name = "plantInfo"
    allowed_domains = ["https://jardinage.ooreka.fr/"]
    start_urls = []

    def __init__(self, url = None):
        self.url = url 

    def start_requests(self):
        if self.url: 
                yield self.make_requests_from_url(self.url)

    def parse(self, response):
        yield {
            'species' : response.xpath('//*[@id="fiches_plantes"]/h1/text()').get(),
            'picUrl' : response.xpath('//*[@id="image-0"]/a/img/@src').get(),
            'decription' : response.xpath('//*[@id="fiches_plantes"]/div[2]/div[2]/div[1]/p[1]/text()').get(),
            'latinName' : response.xpath('//*[@id="resume_plante"]/div[1]/ul/li[2]/p[2]/text()').get(),
            'family' : response.xpath('//*[@id="resume_plante"]/div[1]/ul/li[3]/p[2]/text()').get(),
            #'type' : Arbuste à fleurs | Arbuste fruitier |Plante (.replace <p> "")
            #'vegetation' : Vivace
            #'height' : 1 à 5 m
            #'width' : 1 à3 (attention try catch) (null)
            'careLevel' : re.sub('\s+', '', response.xpath('//*[@id="resume_plante"]/div[3]/ul/li[1]/div/span/text()')[1].get()),
            'waterNeed' : re.sub('\s+', '', response.xpath('//*[@id="resume_plante"]/div[3]/ul/li[2]/div/span/text()')[1].get()),
            'growth' : re.sub('\s+', '', response.xpath('//*[@id="resume_plante"]/div[3]/ul/li[3]/div/span/text()')[0].get()),
            'coldResitance' : re.sub('\s+', '', response.xpath('//*[@id="resume_plante"]/div[3]/ul/li[5]/div/span/text()')[1].get()),
            #'soilType' : Sol argileux
            'sunNeed' : re.sub('\s+', '', response.xpath('//*[@id="resume_plante"]/div[4]/ul/li[1]/div/div/text()')[1].get()),
            #'indoorUse' : Véranda
            #'outdoorUse' : Balcon ou terrasse
            #'plantationMonths' : Avril, Mai, Juin, Julliet, Aout (list)
            #'whereToPlant' : Plantez-le dans un gros 
            'pest' : response.xpath('//*[@id="fiches_plantes"]/div[2]/div[2]/div[10]/div[8]/div/p').getall()[1],
            #'ecologicalTips' : (null)
            #'history' : (null) tableau avec un paragraphe par case
        
        
        
        
        }
