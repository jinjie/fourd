import scrapy
from fourd.items import FourdItem

class FourdSpider(scrapy.Spider) :
    name = "fourd"
    allowed_domains = ["www.singaporepools.com.sg"]
    start_urls = ["http://www.singaporepools.com.sg/DataFileArchive/Lottery/Output/fourd_result_draw_list_en.html"]
    
    def parse(self, response) :
        
        dates = response.xpath("//select/option")
        
        for date in dates :
            url = "http://www.singaporepools.com.sg/en/4d/Pages/Results.aspx?" + date.xpath("@querystring").extract()[0]
            
            yield scrapy.Request(url, callback=self.parse_draw_page)
        
        pass
        
    def parse_draw_page(self, response) :
        
        item = FourdItem()
        
        item["draw_date"] = response.xpath("//th[@class='drawDate']/text()").extract()[0]

        item["draw_no"] = response.xpath("//th[@class='drawNumber']/text()").extract()[0].replace("Draw No. ", "")
    
        item["first"] = response.xpath("//td[@class='tdFirstPrize']/text()").extract()[0]
        item["second"] = response.xpath("//td[@class='tdSecondPrize']/text()").extract()[0]
        item["third"] = response.xpath("//td[@class='tdThirdPrize']/text()").extract()[0]
    
        item["starters"] = []
        
        for number in response.xpath("//tbody[@class='tbodyStarterPrizes']//td/text()") :
            item["starters"].append(number.extract())

        item["consolations"] = []
        
        for number in response.xpath("//tbody[@class='tbodyConsolationPrizes']//td/text()") :
            item["consolations"].append(number.extract())
            
        yield item
        