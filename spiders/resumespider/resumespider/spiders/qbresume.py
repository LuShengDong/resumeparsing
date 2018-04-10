# -*- coding: utf-8 -*-
import scrapy
import cssutils
from resumespider.items import ResumespiderItem


class QbresumeSpider(scrapy.Spider):
    name = 'qbresume'
    allowed_domains = ['cv.qiaobutang.com']
    start_urls = ['http://cv.qiaobutang.com/tpl/']

    def parse(self, response):
        movies = response.xpath('//ul[@class="template-list-ul"]/li')
        for each_movie in movies:
            href = each_movie.xpath('./div[@class="tp-li-right"]/p/a/@href').extract()[0]
            yield response.follow(href, self.parse_resume)
        next_page = response.xpath('//a[@class="next"]/@href').extract()[0]
        yield response.follow(next_page, self.parse)

    def parse_resume(self, response):
        contents = response.xpath('//div[@class="inner_resume"]//span')
        result = ''
        for content in contents:
            line = ''
            text = content.xpath('text()').extract()
            if len(text) == 0:
                continue
            text = text[0]
            css = content.xpath('@style').extract()[0]
            font_size = cssutils.parseStyle(css).getProperty('font-size').value
            font_size = font_size.replace('pt', '')
            line += '{'+font_size+'}'
            line += text
            result += line+'\n'

        item = ResumespiderItem()
        item['title'] = response.xpath('//title/text()').extract()[0]
        item['content'] = result
        yield item

