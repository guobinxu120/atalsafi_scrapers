# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from collections import OrderedDict
import yaml, requests
import os, requests, re, random, time, csv
from json import loads

class luminaire_frSpider(Spider):
    name = "justcars_com_au"
    # start_urls = ['https://www.leroymerlin.fr/v3/p/produits/decoration-eclairage/ampoule-et-led/ampoule-connectee-et-intelligente-l1500733940']
    start_urls = ['https://www.justcars.com.au/cars-for-sale/search']
    count = 0
    result_data_list = []
    total_count = 0

    url_list = []
    use_selenium = False

    headers = ['title', 'state', 'post code','detail url', 'make','model', 'price','phone number']
    # --------------- Get list of proxy-----------------------#



    def start_requests(self):

        f2 = open('result_justcars_com_au_urls.csv')

        csv_items = csv.DictReader(f2)
        cat_data = []

        f0 = open("result_justcars_com_au_new.csv","wb")


        for i, row in enumerate(csv_items):
            cat_data.append(row['url'])


        # missing_urls = []
        #
        # writer = csv.writer(f0, delimiter=',',quoting=csv.QUOTE_ALL)
        # # writer.writerow(spider.headers)
        #
        # f1 = open('result_justcars_com_au.csv')
        #
        # csv_items1 = csv.DictReader(f1)
        #
        # for j, row1 in enumerate(csv_items1):
        #     row1['detail url'] = row1['detail url'].replace('https://www.justcars.com.au/', 'https://www.justcars.com.au')
        #     writer.writerow(row1.values())
        # f0.close()
        #     # if not row1['detail url'].replace('https://www.justcars.com.au/', '') in cat_data:
        #     #     missing_urls.append(row1['detail url'].replace('https://www.justcars.com.au/', ''))
        # f1.close()

        for c in cat_data:
            yield Request('https://www.justcars.com.au/' + c, callback=self.parse_product, dont_filter=True)

        # yield Request('https://www.justcars.com.au//cars-for-sale/1935-buick-sedan/JCMD5039053', callback=self.parse_product)

    def parse_product(self, response):
        item = OrderedDict()
        for h in self.headers:
            item[h] = ''

        name = response.xpath('//div[@class="ja-ad-title ja-ad-full__title ja-ad-full__component"]/div/h1/text()').extract_first()
        item['title'] = name

        location = response.xpath('//a[@class="ja-ad-full__map icon duk-icon-map-marker"]/text()').extract_first()
        item['state'] = location.split(', ')[0]
        item['post code'] = location.split(', ')[-1]
        item['detail url'] = response.url


        ja_table = response.xpath('//table[@class="ja-table"]/tbody/tr')
        for ja in ja_table:
            name = ja.xpath('./td[1]/text()').extract_first()
            val = ja.xpath('./td[2]/text()').extract_first()
            if name == 'Make':
                item['make'] = val
            elif name == 'Model':
                item['model'] = val
            elif name == 'Price':
                item['price'] = val

        image_tag = response.xpath('//div[@class="ja-gallery__list js-ja-gallery__list"]//img/@data-src').extract()
        for i, img in enumerate(image_tag):
            imgName = 'image_url{}'.format(str(i + 1))
            if imgName not in self.headers:
                self.headers.append(imgName)

            item[imgName] = img

        phone_num_url = response.xpath('//div[@class="private-message-form__show-num-wrapper"]/div/a/@href').extract_first()
        if phone_num_url:
            yield Request(response.urljoin(phone_num_url), callback=self.parse_get_phone_number, meta={'item': item}, dont_filter=True)
        else:
            self.total_count += 1
            print 'total count:' + str(self.total_count)

            self.result_data_list.append(item)
            yield item

    def parse_get_phone_number(self, response):
        item = response.meta['item']
        content = response.xpath('//textarea/text()').extract_first()
        tel = ''
        if content and ('tel:' in content):
            tel = content.split('tel:')[-1]
            if tel:
                tel = tel.split('\\u')[0]
                if tel:
                    item['phone number'] = tel
        self.total_count += 1
        print 'total count:' + str(self.total_count)
        self.result_data_list.append(item)
        yield item
