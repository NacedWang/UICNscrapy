# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy import Selector

from uicn.items import UicnItem


class UicnspiderSpider(scrapy.Spider):
    name = 'uicnspider'
    allowed_domains = ['s.ui.cn']
    page = 1
    base_url = 'https://s.ui.cn/index.html?type=experience&keywords=&other_w=&t=&p='
    start_urls = [base_url + str(page)]

    def parse(self, response):
        # 使用bs4解析导出
        # yield from self.analysisByBs4(response)

        # 使用scrapy 自带Selector导出
        yield from self.analysisBySelector(response)

        # 前100页
        if self.page < 100:
            self.page += 1
            yield scrapy.Request(self.base_url + str(self.page), callback=self.parse)

    # 使用bs4解析导出
    def analysisBySelector(self, response):
        # sel = Selector(text=response.css('.post-works').get(), type="html")
        # nodes = sel.xpath('//li').extract()
        nodes = response.css('.post-works li').extract()
        for node in nodes:
            try:
                item = UicnItem()
                itemSelect = Selector(text=node, type="html")
                # 方式1 xpath
                # title = itemSelect.xpath('//h4/text()').extract()[0]
                # 方式2 css
                title = itemSelect.css('h4::text').extract_first()
                # 方式1 xpath
                # url = itemSelect.xpath('//div//@href')[0].extract()
                # 方式2 css
                url = itemSelect.css('.cover a::attr(href)').extract_first()
                item['title'] = title
                item['url'] = url
                item['id'] = url.replace('https://www.ui.cn/detail/', '').replace('.html', '')
                yield item
            except Exception as e:
                print("build item error :", str(e))

    # 使用bs4解析导出 (慢)
    def analysisByBs4(self, response):
        soup = BeautifulSoup(response.body.decode(), 'html.parser')
        ul = soup.find('ul', attrs={'class': 'post post-works mtv cl'})
        lists = ul.find_all('li')
        for node in lists:
            try:
                item = UicnItem()
                info = node.find('div', attrs={'class': 'info'})
                cover = node.find('div', attrs={'class': 'cover pos'})
                title = info.find('h4', attrs={'class': 'title download ellipsis'})
                url = cover.find('a')['href']
                item['title'] = title.text
                item['url'] = url
                item['id'] = url.replace('https://www.ui.cn/detail/', '').replace('.html', '')
                yield item
            except Exception as e:
                print("build item error :", str(e))
