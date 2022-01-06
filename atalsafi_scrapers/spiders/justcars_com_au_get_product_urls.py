# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from collections import OrderedDict
import yaml, requests
import os, requests, re, random, time, csv
from json import loads

class luminaire_frSpider(Spider):
    name = "justcars_com_au_get_product_urls"
    # start_urls = ['https://www.leroymerlin.fr/v3/p/produits/decoration-eclairage/ampoule-et-led/ampoule-connectee-et-intelligente-l1500733940']
    start_urls = ['https://www.justcars.com.au/cars-for-sale/search']
    count = 0
    result_data_list = {}
    total_count = 0
    use_selenium = True
    url_list = []

    page_count = 1

    headers = ['productname', 'state', 'Code ean','url', 'price','price unit', 'sku','availability', 'productimg1', 'productimg2', 'productimg3', 'productimg4', 'productimg5', 'categorie','sub_categorie', 'features', 'productdescriptionshort']
    # --------------- Get list of proxy-----------------------#



    def start_requests(self):
        yield Request('https://www.justcars.com.au/cars-for-sale/search', callback=self.parse_products)

    def parse_products(self, response):
        item_urls = response.xpath('//div[@class="blazy-carousel"]/a/@href').extract()
        for item_url in item_urls:
            self.total_count += 1
            print('total count :' + str(self.total_count))

            yield {'url': item_url}
        self.page_count += 1
        if len(item_urls) >= 12:
            yield Request('https://www.justcars.com.au/cars-for-sale/search?p={}'.format(self.page_count), callback=self.parse_products)
