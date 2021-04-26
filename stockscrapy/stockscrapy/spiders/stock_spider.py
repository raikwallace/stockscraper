import scrapy
import scrapy_splash


class StockSpider(scrapy.Spider):
    name = "stock_spider"

    def start_requests(self):
        yield scrapy_splash.SplashRequest(
                url=self.url, callback=self.parse, endpoint='render.html'
            )

    def parse(self, response):
        title = response.xpath('//div[@class="buy"]/a/text()').get()
        return { 'url': self.url, 'buy': str(title).replace('\n', '').strip()}