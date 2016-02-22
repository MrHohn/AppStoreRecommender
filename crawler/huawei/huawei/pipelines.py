# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class HuaweiPipeline(object):
	def __init__(self):
		self.file = open('huawei.dat', 'wb')
		
	def process_item(self, item, spider):
		val = "{0}\t{1}\t{2}\t{3}\n".format(item['appid'], item['title'], item['thumbnail'], item['recommended'])
		self.file.write(val)
		return item