# -*- coding: utf-8 -*-
import scrapy
from sougouspider.items import SougouspiderItem


class CellcorpusSpider(scrapy.Spider):
    name = 'cellcorpus'
    allowed_domains = ['sogou.com']
    url_dictionary = {
        'https://pinyin.sogou.com/dict/cate/index/1': 'pro_natural_sci',
        'https://pinyin.sogou.com/dict/cate/index/76': 'pro_society_sci',
        'https://pinyin.sogou.com/dict/cate/index/96': 'pro_engineer',
        'https://pinyin.sogou.com/dict/cate/index/127': 'pro_agriculture',
        'https://pinyin.sogou.com/dict/cate/index/132': 'pro_medical',
        'https://pinyin.sogou.com/dict/cate/index/154': 'pro_art',
        'https://pinyin.sogou.com/dict/cate/index/31': 'pro_human'
    }
    start_urls = url_dictionary.keys()

    def parse(self, response):
        file_urls = response.xpath('//div[@class="dict_detail_show"]//a/@href').extract()
        for url in file_urls:
            si = SougouspiderItem()
            si['file_urls'] = [url]
            si['files'] = 'society'
            yield si

