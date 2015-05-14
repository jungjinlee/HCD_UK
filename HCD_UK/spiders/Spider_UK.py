from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

import MySQLdb

# here is a test comment

class Spider_UK(CrawlSpider):
    # MySQL Settings
    db = MySQLdb.connect("localhost", "root", "apmsetup", "HCD_UK")
    cursor = db.cursor()

    # Scrapy Settings
    name = 'Spider_UK'
    allowed_domains = ['supremecourt.uk']
    start_urls = ['https://www.supremecourt.uk/decided-cases']

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=('//table[@class="caselist-test"]//a/@href'))),
        Rule(SgmlLinkExtractor(allow=('https://www.supremecourt.uk/cases/',)), callback='parse_item'),
    )

    # Crawl (by Scrapy) & Restore (by MySQL)
    def parse_item(self, response):
        sel = Selector(response)
        print '====================================='
        judgment_date = sel.xpath('/html/body/div[2]/div/div/div[4]/div[1]/div/section/p[1]/text()').extract()
        citation_number = sel.xpath('/html/body/div[2]/div/div/div[4]/div[1]/div/section/p[2]/text()').extract()
        case_id = sel.xpath('/html/body/div[2]/div/div/div[4]/div[1]/div/section/p[3]/text()').extract()
        justices = sel.xpath('/html/body/div[2]/div/div/div[4]/div[1]/div/section/p[4]/text()').extract()

        judgment_date = str(judgment_date[0])
        citation_number = str(citation_number[0])
        case_id = str(case_id[0])
        justices = str(justices[0])

        try:
            self.cursor.execute("INSERT INTO case_info (judgment_date, citation_number, case_id, justices) VALUES ('%s','%s','%s','%s')" % (judgment_date, citation_number, case_id, justices))
        except:
            print 'Error'