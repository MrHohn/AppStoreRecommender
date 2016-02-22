import scrapy
import re
from scrapy.selector import Selector
from huawei.items import HuaweiItem

class HuaweiSpider(scrapy.Spider):
	name = "huawei"
	allowed_domains = ["huawei.com"]
	maxPages = 2;

	start_urls = [
		"http://appstore.huawei.com/more/all/1", 
		# "http://appstore.huawei.com/more/recommend/1", 
		# "http://appstore.huawei.com/more/soft/1", 
		# "http://appstore.huawei.com/more/game/1", 
		# "http://appstore.huawei.com/more/newPo/1", 
		# "http://appstore.huawei.com/more/newUp/1"
	]

	# def start_requests(self):
	# 	for url in self.start_urls:
	# 		yield scrapy.Request(url, self.parse, meta={
	# 			'splash': {
	# 				'endpoint': 'render.html',
	# 				'args': {'wait': 0.5}
	# 			}
	# 		})


	def parse(self, response):
		page = Selector(response)
		
		# crawl all the app url form the home page
		hrefs = page.xpath('//h4[@class="title"]/a/@href')

		for href in hrefs:
			url = href.extract()
			yield scrapy.Request(url, callback=self.parseItem)

		yield scrapy.Request(self.find_next_page(response.url), callback=self.parse)


	def parseItem(self, response):
		page = Selector(response)
		item = HuaweiItem()

		# crawl appstore item
		item['title'] = page.xpath('//ul[@class="app-info-ul nofloat"]/li/p/span[@class="title"]/text()').extract_first().encode('utf-8')
		item['url'] = response.url
		item['appid'] = re.match(r'http://.*/(.*)', item['url']).group(1)
		item['intro'] = page.xpath('//meta[@name="description"]/@content').extract_first().encode('utf-8')
		item['thumbnail'] = page.xpath('//ul[@class="app-info-ul nofloat"]/li[@class="img"]/img[@class="app-ico"]/@lazyload').extract_first()

		# now crawl all the recommendations for this app
		divs = page.xpath('//div[@class="open-info"]')
		recomm = ""
		for div in divs:
			url = div.xpath('./p[@class="name"]/a/@href').extract_first()
			recommended_appid = re.match(r'http://.*/(.*)', url).group(1)
			name = div.xpath('./p[@class="name"]/a/text()').extract_first().encode('utf-8')
			recomm += "{0}:{1},".format(recommended_appid, name)
		item['recommended'] = recomm
		yield item


	def find_next_page(self, url):
		try:
			page_num_str = url.split('/')[-1]
			page_num = int(page_num_str) + 1
			# limit page count for testing
			# if page_num > 1: # crawl only specified number of pages
			#	return "http://google.com"
			if page_num <= self.maxPages:
				url = url[:-len(page_num_str)] + str(page_num)
				return url
			else:
				return "http://google.com"
		except ValueError:
			print "### page cannot be handled"
			print url
			return "http://google.com"