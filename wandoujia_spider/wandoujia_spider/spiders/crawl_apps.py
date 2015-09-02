# -*- coding: utf-8 -*-
import sys
import re
reload(sys)
sys.setdefaultencoding("utf-8")
import scrapy
from wandoujia_spider.items import AppItem

class CrawlAppSpider(scrapy.Spider):
  name = "crawl_app"
  start_urls = (
    'http://t.wdjcdn.com/upload/www/wandoujia.com/nav.js?1',
  )

  def parse(self, response):
    tokens = response.body.split("<a class=\\\"cate-link\\\"")
    for token in tokens:
      sub_tokens = token.split("</a> <ul> <li")
      category = sub_tokens[0].split("\"")[1][5:-1]
      if category == "class=":
        continue
      url = "http://www.wandoujia.com/tag/" + category
      yield scrapy.http.Request(url=url,
          callback=lambda response, category=category: self.CrawlAppPage(response, category))

  # 获取某个分类下的页数
  def CrawlAppPage(self, response, category):
    pages = response.selector.xpath('/html/body/div[@class="container"]/div[@class="pages"]/span')
    page_num = int(pages[-2].xpath('a/strong/text()').extract()[0])
    for i in range(1, page_num + 1):
      yield scrapy.http.Request(url=response.url + "/" + str(i),
          callback=lambda response, category=category: self.CrawlApp(response, category))

  def CrawlApp(self, response, category):
    app_list = response.selector.xpath('/html/body/div[@class="container"]/ul[@id="j-tag-list"]/li')
    for app in app_list:
      title = app.xpath('div[@class="app-desc"]/a/text()').extract()
      yield AppItem({"category": category, "name": title[0]})

