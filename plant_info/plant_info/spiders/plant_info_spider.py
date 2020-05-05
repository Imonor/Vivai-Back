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
            'species': response.xpath('//*[@id="fiches_plantes"]/h1/text()').get(),
            'family': response.xpath('//*[@id="resume_plante"]/div[1]/ul/li[3]/p[2]/text()').get(),
            'picUrl': response.xpath('//*[@id="image-0"]/a/img/@src').get(),
            'waterNeed': re.sub('\s+', '', response.xpath('//*[@id="resume_plante"]/div[3]/ul/li[2]/div/span/text()')[1].get()),
            'growth': re.sub('\s+', '', response.xpath('//*[@id="resume_plante"]/div[3]/ul/li[3]/div/span/text()')[0].get()),
            'coldResistance': re.sub('\s+', '', response.xpath('//*[@id="resume_plante"]/div[3]/ul/li[5]/div/span/text()')[1].get()),
            'sunNeed': re.sub('\s+', '', response.xpath('//*[@id="resume_plante"]/div[4]/ul/li[1]/div/div/text()')[1].get()),
            'soilType': re.sub('\s+', '', response.xpath('//*[@id="resume_plante"]/div[3]/ul/li[6]/div/span/text()').get()),
            'soilHumidity': re.sub('\s+', '', response.xpath('//*[@id="resume_plante"]/div[3]/ul/li[8]/div/span/text()').get()),
        }
