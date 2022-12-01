import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_links = response.css('a[href^="/pep-"]')
        for link in all_links:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        data = {
            'number': int(response.css('li:contains("PEP Index") + li').css(
                          'li::text').get()[4:]),
            'name': response.css('h1.page-title::text').get().replace(
                response.css('li:contains("PEP Index") + li').css(
                    'li::text').get(), '').replace('–', '').strip(),
            'status': response.css('dt:contains("Status") + dd').css(
                        'abbr::text').get()
        }
        yield PepParseItem(data)
