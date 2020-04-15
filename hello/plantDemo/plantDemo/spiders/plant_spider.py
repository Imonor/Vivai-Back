#type in 2:Python:
#PS C:\PLD SMART\Vivai-Back\hello\plantDemo\plantDemo\spiders> scrapy crawl plants

import scrapy

class PlantsSpider(scrapy.Spider):

    name = "plants"

    def start_requests(self):
        urls = [
        'https://jardinage.ooreka.fr/plante/voir/16/basilic',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield {
            'nom': response.xpath('//*[@id="fiches_plantes"]/h1/text()').extract(),
        }
        yield {
            'famille': response.xpath('//*[@id="resume_plante"]/div[1]/ul/li[3]/p[2]/text()').extract(),
        }
        yield {
            'entretien': response.xpath('//*[@id="resume_plante"]/div[3]/ul/li[1]/div/span/text()').extract()[1:2],
        }
        yield {
            'besoinEau': response.xpath('//*[@id="resume_plante"]/div[3]/ul/li[2]/div/span/text()').extract()[1:2],
        }
        yield {
            'croissance': response.xpath('//*[@id="resume_plante"]/div[3]/ul/li[3]/div/span/text()').extract()[1:2],
        }
        yield {
            'resistanceFroid': response.xpath('//*[@id="resume_plante"]/div[3]/ul/li[5]/div/span/text()').extract()[1:2],
        }
        yield {
            'exposition': response.xpath('//*[@id="resume_plante"]/div[4]/ul/li[1]/div/div/text()').extract()[1:2],
        }
        yield {
            'hauteurMaturite': response.xpath('//*[@id="resume_plante"]/div[2]/ul/li[6]/div/span/text()').extract(),
        }
        yield {
            'largeurMaturite': response.xpath('//*[@id="resume_plante"]/div[2]/ul/li[7]/div/span/text()').extract(),
        }

        #with open('urls.txt', 'w') as f:
        #    for u in img_urls:
        #        f.write(u + "\n")