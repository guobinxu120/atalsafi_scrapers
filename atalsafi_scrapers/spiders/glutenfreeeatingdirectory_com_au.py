# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from collections import OrderedDict
import yaml, requests
import os, requests, re, random, time, csv
from json import loads

class luminaire_frSpider(Spider):
    name = "glutenfreeeatingdirectory_com_au"
    # start_urls = ['https://www.leroymerlin.fr/v3/p/produits/decoration-eclairage/ampoule-et-led/ampoule-connectee-et-intelligente-l1500733940']
    start_urls = ['https://www.glutenfreeeatingdirectory.com.au/restaurants',
                  'https://www.glutenfreeeatingdirectory.com.au/paleo',
                  'https://www.glutenfreeeatingdirectory.com.au/manufacturers']
    count = 0
    result_data_list = {}
    total_count = 0

    url_list = []

    headers = ['productname', 'brand', 'Code ean','url', 'price','price unit', 'sku','availability', 'productimg1', 'productimg2', 'productimg3', 'productimg4', 'productimg5', 'categorie','sub_categorie', 'features', 'productdescriptionshort']
    # --------------- Get list of proxy-----------------------#



    def start_requests(self):
        r = requests.delete('https://www.lowes.com/wcs/resources/store/10151/member/address/335547551/v1_0')
        content = r.content

        r = requests.get('https://foursquare.com/explore?q=Top%20Picks&near=New%20York')
        content = r.content
        wsid = r.cookies._cookies['.foursquare.com']['/']['bbhive'].value.split('%3')[0]
        productInfo = loads(re.findall('fourSq.config.explore.response = (.*);fourSq.config.explore.respondToSuggestedBounds', content)[0])

        total_count = productInfo['group']['totalResults']

        keyword = 'Top Picks'
        if total_count > 0:
            results = productInfo['group']['results']
            for result in results:
                venue = result['venue']
                name = venue['name']
                shortName = venue['categories'][0]['shortName']

                anchor = ''
                if 'menu' in venue.keys():
                    anchor = venue['menu']['anchor']

                description = ''
                if anchor:
                    description = '{} • {}'.format(shortName, anchor)
                else:
                    description = shortName

                location = venue['location']
                address = location['address']
                crossStreet = ''
                if 'crossStreet' in location.keys():
                    crossStreet = location['crossStreet']
                else:
                    pass
                city = location['city']
                if crossStreet:
                    real_address = '{} ({}), {}'.format(address, crossStreet, city)
                else:
                    real_address = '{} , {}'.format(address, city)
            if total_count > len(results):
                loop_count = int(total_count / 30)
                if total_count % 30 > 0:
                    loop_count += 1
                oauth_token = ''
                config_api = yaml.load(re.findall('window.fourSq.config.api = (.*); window.fourSq.config.user = ', content)[0])
                oauth_token = config_api['API_TOKEN']

                sw = productInfo['suggestedBounds']['sw']
                ne = productInfo['suggestedBounds']['ne']

                keyword_again = '+'.join(keyword.split(' '))

                payload = {'accept': 'application/json, text/javascript, */*; q=0.01',
                           'accept-encoding': 'gzip, deflate, br',
                           'cookie':'__utmc=51454142; __utmz=51454142.1546602355.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); bbhive=1CFWSQDTMXD3QTUUGABFKRQWOS5IM0%3A%3A1609674355; __gads=ID=2e51ca9d229bca54:T=1546602443:S=ALNI_MYjATJD-mCKhtUQMBctZrijftspmw; _ga=GA1.2.343575887.1546602355; _gid=GA1.2.2001749403.1546603822; __utma=51454142.343575887.1546602355.1546608027.1546612744.3; __utmt=1; __utmb=51454142.2.10.1546612744; _gat=1; _px2=eyJ1IjoiYjIzODEyNzAtMTAyZS0xMWU5LWFlNjctYTdkYmU5MzA4ZjQ0IiwidiI6IjQ5YmM2ODgwLTEwMTYtMTFlOS1iMmI2LTRiOWJiYTNkMWRlNyIsInQiOjE1NDY2MTMxMzYzNDYsImgiOiJhNTM1ODQyODU2N2FlNWUwOTNkZDQzMWJkYjUzNTZiZTk3NmFhMTQ0YmUwOWRiYjgzYjZkZDkzNGQ4YzkwMGQ5In0=',
                           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

                for i in range(loop_count):
                    request_url = 'https://api.foursquare.com/v2/search/recommendations?locale=en&explicit-lang=false&v=20190104' \
                                  '&m=foursquare&query={}' \
                                  '&limit=30&offset=30' \
                                  '&sw={}%2C{}' \
                                  '&ne={}%2C{}' \
                                  '&wsid={}' \
                                  '&oauth_token={}'.format(keyword_again,
                                                          sw['lat'], sw['lng'],
                                                          ne['lat'], ne['lng'],
                                                          wsid,
                                                          oauth_token)
                    next_request = requests.get(request_url, params=payload)
                    productInfo = next_request['response']
                    results = productInfo['group']['results']
                    for result in results:
                        venue = result['venue']
                        name = venue['name']
                        shortName = venue['categories'][0]['shortName']

                        anchor = ''
                        if 'menu' in venue.keys():
                            anchor = venue['menu']['anchor']

                        description = ''
                        if anchor:
                            description = '{} • {}'.format(shortName, anchor)
                        else:
                            description = shortName

                        location = venue['location']
                        address = location['address']
                        crossStreet = location['crossStreet']
                        city = location['city']

                        real_address = '{} ({}), {}'.format(address, crossStreet, city)


        for url in self.start_urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        urls = response.xpath('//div[contains(@class,"col-md-12 big-list one-quarter")]/ul/li/a')
        for i, url_tag in enumerate(urls):
            url = url_tag.xpath('./@href').extract_first()
            category = url_tag.xpath('./text()').extract_first()
            yield Request(response.urljoin(url), self.parse_products,
                          meta={'next_count': 1, 'cat': category},
                          dont_filter=True)
            # # for test
            # break



    def parse_products(self, response):
        item_urls = response.xpath('//div[@class="result"]/a/@href').extract()
        for item_url in item_urls:
            yield Request(response.urljoin(item_url), self.parse_product,
                          meta={'cat': response.meta['cat']},
                          dont_filter=True)

            # # for test
            # break

        next_tag = response.xpath('//div[@class="page-list"]/div/a[@rel="next"]/@href').extract_first()
        if next_tag:
            yield Request(response.urljoin(next_tag), self.parse_products,
                          meta={'next_count': 1, 'cat': response.meta['cat']},
                          dont_filter=True)

    def parse_product(self, response):

        name = response.xpath('//h1[@itemprop="name"]/text()').extract_first()
        logo_image = response.xpath('//img[@itemprop="image"]/@src').extract_first()

        links = response.xpath('//ul[@class="links"]/li/a/@href').extract()
        web_url = ''
        email = ''
        for link in links:
            if 'www.facebook.com' not in link:
                if 'mailto:' in link:
                    email = link.replace('mailto:', '')
                else:
                    web_url = link

        phone = response.xpath('//gf-call-button/@number').extract_first()
        cat = response.meta['cat']

        descs = response.xpath('//div[@class="description"]//text()').extract()
        desc_list = []
        description = ''
        for d in descs:
            if d:
                d = d.strip()
                if d:
                    desc_list.append(d)
        if desc_list:
            description = '\n'.join(desc_list)

        item = OrderedDict()
        item['name'] = name
        item['logo'] = logo_image
        item['email'] = email
        item['phone'] = phone
        item['web address'] = web_url
        item['category'] = cat
        item['description'] = description

        self.total_count += 1
        print('total count: ' + str(self.total_count))

        yield item
