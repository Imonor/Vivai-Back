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

        typeItems = response.xpath('//*[@id="resume_plante"]/div[1]/ul/li[4]//p/text()').extract()
        typeString = ""
        for p  in typeItems[1:] :
            p = p.replace('\t','').replace('\n','')
            typeString = typeString + p

        def data_parse(xpathResponse) :
            items = response.xpath(xpathResponse).extract()
            itemString = ""
            for p  in items :
                p = p.replace('\t','').replace('\n','')
                if p :
                    itemString = itemString + p
            return itemString

        def data_clean(xpathResponse) :
            items = response.xpath(xpathResponse).extract()
            for p in items :
                p = re.sub('<[^>]+>', '', p)
            return items

        def height_test() :
            default = ""

            if any("Hauteur" in s for s in response.xpath('//*[@id="resume_plante"]/div[2]/ul/li[4]/p/text()').extract()) :
                return re.sub('<[^>]+>', '', response.xpath('//*[@id="resume_plante"]/div[2]/ul/li[4]/div/span').extract()[0]).strip('\n').strip('\t').strip('\n')
            elif any("Hauteur" in s for s in response.xpath('//*[@id="resume_plante"]/div[2]/ul/li[6]/p/text()').extract()) :
                return re.sub('<[^>]+>', '', response.xpath('//*[@id="resume_plante"]/div[2]/ul/li[6]/div/span').extract()[0]).strip('\n').strip('\t').strip('\n')
            elif any("Hauteur" in s for s in response.xpath('//*[@id="resume_plante"]/div[2]/ul/li[5]/p/text()').extract()) :
                return re.sub('<[^>]+>', '', response.xpath('//*[@id="resume_plante"]/div[2]/ul/li[5]/div/span').extract()[0]).strip('\n').strip('\t').strip('\n')
            else :
                return default

        def width_test() :
            default = ""
            if any("Largeur" in s for s in response.xpath('//*[@id="resume_plante"]/div[2]/ul/li[6]/p').extract()) :
                return re.sub('<[^>]+>', '', response.xpath('//*[@id="resume_plante"]/div[2]/ul/li[6]/div/span').extract()[0]).strip('\n').strip('\t').strip('\n')
            if any("Largeur" in s for s in response.xpath('//*[@id="resume_plante"]/div[2]/ul/li[7]/p').extract()) :
                return re.sub('<[^>]+>', '', response.xpath('//*[@id="resume_plante"]/div[2]/ul/li[7]/div/span').extract()[0]).strip('\n').strip('\t').strip('\n')

            else :
                return default

        def outdoor_test() :
            default = ""

            if any("ext" in s for s in response.xpath('//*[@id="resume_plante"]/div[4]/ul/li[3]/p').extract()) :
                return data_parse('//*[@id="resume_plante"]/div[4]/ul/li[3]/div/span/text()')
            if any("ext" in s for s in response.xpath('//*[@id="resume_plante"]/div[4]/ul/li[2]/p').extract()) :
                return data_parse('//*[@id="resume_plante"]/div[4]/ul/li[2]/div/span/text()')
            else :
                return default

        def indoor_test() :
            default = ""

            if any("int" in s for s in response.xpath('//*[@id="resume_plante"]/div[4]/ul/li[2]/p').extract()) :
                return data_parse('//*[@id="resume_plante"]/div[4]/ul/li[2]/div/span/text()')
            else :
                return default

        def where_test() :
            default = ""

            if any("Où" in s for s in response.xpath('//*[@id="fiches_plantes"]/div[2]/div[2]/div[10]/div[3]/div/h3[1]/text()').extract()) :
                return response.xpath('//*[@id="fiches_plantes"]/div[2]/div[2]/div[10]/div[3]/div/h3[1]/following-sibling::p').extract()[0]
            if any("Où" in s for s in response.xpath('//*[@id="fiches_plantes"]/div[2]/div[2]/div[10]/div[3]/div/h3[2]/text()').extract()) :
                return response.xpath('//*[@id="fiches_plantes"]/div[2]/div[2]/div[10]/div[3]/div/h3[2]/following-sibling::p').extract()[0]
            else :
                return default

        def pest_test() :
            default = ""

            if any("Maladies" in s for s in response.xpath('//*[@id="conseils-ecologiques"]/text()').extract()[0]) :
                return response.xpath('//*[@id="conseils-ecologiques"]/following-sibling::p').extract()
            else :
                return default

        def ecological_test() :
            default = "HHH"

            if any("Conseils" in s for s in response.xpath('//*[@id="conseils-ecologiques"]/text()').extract()) :
                return data_clean('//*[@id="fiches_plantes"]/div[2]/div[2]/div[10]/div[12]/div//p')
                #('//*[@id="conseils-ecologiques"]/following-sibling::div')
            else :
                return default
        yield {
            'species' : response.xpath('//*[@id="fiches_plantes"]/h1/text()').get(),
            'picUrl' : response.xpath('//*[@id="image-0"]/a/img/@src').get(),
            'description' : response.xpath('//*[@id="fiches_plantes"]/div[2]/div[2]/div[1]/p[1]/text()').get(),
            'latinName' : response.xpath('//*[@id="resume_plante"]/div[1]/ul/li[2]/p[2]/text()').get(),
            'family' : response.xpath('//*[@id="resume_plante"]/div[1]/ul/li[3]/p[2]/text()').get(),
            'type' : typeString,
            'vegetation' : data_parse('//*[@id="resume_plante"]/div[2]/ul/li[3]/div//span/text()'),
            'height' : height_test(),
            'width' : width_test(),
            'careLevel' : re.sub('\s+', '', response.xpath('//*[@id="resume_plante"]/div[3]/ul/li[1]/div/span/text()')[1].get()),
            'waterNeed' : re.sub('\s+', '', response.xpath('//*[@id="resume_plante"]/div[3]/ul/li[2]/div/span/text()')[1].get()),
            'growth' : re.sub('\s+', '', response.xpath('//*[@id="resume_plante"]/div[3]/ul/li[3]/div/span/text()')[0].get()),
            'coldResistance' : re.sub('\s+', '', response.xpath('//*[@id="resume_plante"]/div[3]/ul/li[5]/div/span/text()')[1].get()),
            #'soilType' : Sol argileux
            'sunNeed' : re.sub('\s+', '', response.xpath('//*[@id="resume_plante"]/div[4]/ul/li[1]/div/div/text()')[1].get()),
            #'indoorUse' : Véranda
            #'outdoorUse' : Balcon ou terrasse
            #'plantationMonths' : Avril, Mai, Juin, Julliet, Aout (list)
            #'whereToPlant' : Plantez-le dans un gros 
            # 'pest' : response.xpath('//*[@id="fiches_plantes"]/div[2]/div[2]/div[10]/div[8]/div/p').getall()[1],
            #'ecologicalTips' : (null)
            #'history' : (null) tableau avec un paragraphe par case
        }
