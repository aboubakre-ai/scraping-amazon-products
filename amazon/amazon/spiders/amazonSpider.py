import scrapy
from ..items import AmazonItem


class AmazonspiderSpider(scrapy.Spider):
    name = 'amazon'
    page_number = 2
    start_urls = [
        'https://www.amazon.com/s?i=stripbooks&bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&dc&fst=as%3Aoff&qid=1608656450&rnid=1250225011&ref=sr_pg_1',
                  ]

    def parse(self, response):
        items = AmazonItem()
        all_products = response.css(".s-latency-cf-section")
        for i in range (1,len(all_products)):
            product_name = all_products[i].css(".a-color-base.a-text-normal").css("::text").extract()
            product_author = all_products[i].css(".sg-col-12-of-20 .sg-col-12-of-20 .a-size-base+ .a-size-base").css("::text").extract()
            product_price = all_products[i].css(".a-spacing-top-small .a-price-whole").css("::text").extract()
            product_imagelink = all_products[i].css(".s-image::attr(src)").extract()

            items["product_name"] = product_name
            items["product_author"] = [elem.rstrip().lstrip() for elem in product_author]
            items["product_price"] = product_price
            items["product_imagelink"] = product_imagelink

            yield items

        next_page = 'https://www.amazon.com/s?i=stripbooks&bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&dc&page='+str(AmazonspiderSpider.page_number)+'&fst=as%3Aoff&qid=1608656590&rnid=1250225011&ref=sr_pg_'+str(AmazonspiderSpider.page_number)
        if AmazonspiderSpider.page_number <= 50:
            AmazonspiderSpider.page_number += 1
            yield response.follow(next_page, callback = self.parse)
