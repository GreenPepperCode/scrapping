import scrapy

class LNBSpider(scrapy.Spider):
    name = 'lnb_spider'
    start_urls = ['https://www.lnb.fr/elite/stats-engine/?option=player&season=2023&competition=276&type=total&page=1']

    def parse(self, response):
        players_data = []
        table = response.css('table.table-stats')
        for row in table.css('tr')[1:]:
            cols = row.css('td')
            player = {
                "joueur": cols[0].get(),
                "équipe": cols[1].get(),
                # ... extract other fields ...
                "eval": cols[26].get()
            }
            players_data.append(player)

        # Follow pagination links
        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

        # Yield the collected data
        yield {'players_data': players_data}
