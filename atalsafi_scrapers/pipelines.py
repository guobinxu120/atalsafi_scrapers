# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from collections import OrderedDict
import csv

class AtalsafiScrapersPipeline(object):
    def process_item(self, item, spider):
        return item

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        pass

    def spider_closed(self, spider):
        f1 = open("result_justcars_com_au_missing.csv","wb")
        writer = csv.writer(f1, delimiter=',',quoting=csv.QUOTE_ALL)
        writer.writerow(spider.headers)

        for it in spider.result_data_list:
            writer.writerow(it.values())
            # item = OrderedDict()
            # for key in spider.headers:
            #     if key in it.keys():
            #         item[key] = it[key]
            #     else
        f1.close()


        # filepath = 'eat_ch_restaurants.xlsx'
        # if os.path.isfile(filepath):
        #     os.remove(filepath)
        # # workbook = xlsxwriter.Workbook(filepath)
        # workbook = xlsxwriter.Workbook(filepath, {'strings_to_urls': False})
        # sheet = workbook.add_worksheet('sheet')
        # data = spider.result_data_list
        # headers = spider.headers
        # flag =True
        # # headers = []
        # print('---------------Writing in file----------------------')
        # print('total row: ' + str(len(data)))
        #
        # for index, value in enumerate(data.keys()):
        #     if flag:
        #         for col, val in enumerate(headers):
        #             # headers.append(val)
        #             sheet.write(index, col, val)
        #         flag = False
        #     for col, key in enumerate(headers):
        #         # try:
        #             if key in data[value].keys():
        #                 sheet.write(index+1, col, data[value][key])
        #             else:
        #                 sheet.write(index+1, col, '')
        #         # except:
        #         #     continue
        #     print('row :' + str(index))
        #
        # workbook.close()
