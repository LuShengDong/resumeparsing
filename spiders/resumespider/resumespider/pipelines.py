# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs

class ResumespiderPipeline(object):
    def process_item(self, item, spider):
        with codecs.open("resumes/" + item['title'].replace('/', ',') + ".txt", 'w', 'utf-8') as fp:
            fp.write(item['content'])
