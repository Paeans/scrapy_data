# -*- coding: utf-8 -*-
import scrapy
import time


class EventParseSpider(scrapy.Spider):
  name = 'eventparse'
  allowed_domains = ['www.airbnb.com']
  id_list = []
  id_index = 0
  # start_urls = ['https://www.airbnb.com/experiences/120925']
  counter = 0

  def start_requests(self):
    with open('uniq_id.txt', 'r') as id_file:
      for line in id_file:
        self.id_list.append(line.strip())
    yield scrapy.Request(url='https://www.airbnb.com' + self.nextTarget(), callback=self.parse)

  def nextTarget(self):
    return '/experiences/' + str(self.id_list[self.id_index])
  
  def parse(self, response):
    result = {}

    result['host_id'] = str(self.id_list[self.id_index])
    result['event_url'] = response.xpath('//head/meta[@property="og:url"]/@content').get()
    if response.xpath('//h1/div[@class="_1r93ihzp"]/text()').get() == None:
      result['event_title'] = response.xpath('//h2/div[@class="_keicei4"]/text()').get()
      result['address'] = {
          'url': '', 
          'name': response.xpath('//section[@id="Section16"]//section//button[@class="_b0ybw8s"]/text()').get(),
          }
      result['size'] = [
        ['time', 'include', 'language', 'people'], 
        [x.get() for x in 
            response.xpath('//section[@id="Section16"]//section//div[@class="_11vbjbm"]/div[@class="_h6avcp2"]/text()')]]
      result['host'] = [{
        'url': host_info.xpath('div//a/@href').get(), 
        'name': host_info.xpath('div/div/text()').get(),
        'img': host_info.xpath('div//a/img/@src').get(),
        } for host_info in response.xpath('//div[@class="_1t0h0lo"]/div[@class="_ifstn80"]')
        ]
      result['host_img'] = response.xpath('//section[@id="Section16"]//section//div[@class="_4626ulj"]//img/@src').getall()
    else:
      result['event_title'] = response.xpath('//h1/div[@class="_1r93ihzp"]/text()').get()
      event_address = response.xpath('//div/a[@class="_12qaq5ub"]')
      result['address'] = {
          'url': event_address.xpath('@href').get(), 
          'name': event_address.xpath('text()').get(),
          }
      result['size'] = [
        ['time', 'people', 'include', 'language'], 
        [x.get() for x in 
            response.xpath('//div[@class="_hvcs4fi"]/div/div[@class="_z63bg5"]/div/div[@class="_17zvmwh2"]/text()')]]
      result['host'] = [{
        'url': host_info.xpath('div/a/@href').get(), 
        'name': host_info.xpath('div/div/text()').get(),
        'img': host_info.xpath('div//img/@src').get(),
        } for host_info in response.xpath('//section[@id="Section8"]//section//section/div/div[@class="_5he77f"]')
        ]
      result['host_img'] = [x.xpath('@src').get() for x in response.xpath('//div[@class="_4626ulj"]/img')]

    rate_section = response.xpath('//main//div[@class="_dmn8hc"]')
    result['rate'] = {
        'score': rate_section.xpath('div//div[@class="_i5duul"]//div[@class="_1julapm"]/div/div/text()').get(), 
        'number': rate_section.xpath('div//div[@class="_i5duul"]/div/text()').get(),
        'price': rate_section.xpath('div/div/span/text()').get(),
        }

    result['tag'] = [{
        'name': tag_link.xpath('div/div/text()').get(), 
        'url': tag_link.xpath('@href').get()
        } for tag_link in response.xpath('//div[@class="_j6urmsh"]/div[@class="_17p554h"]/a[@class="_12qaq5ub"]')
        ]


    
    yield result
    
    self.id_index = self.id_index + 1
    time.sleep(2);
    if self.id_index < len(self.id_list):
      yield response.follow(self.nextTarget(), self.parse)
    
    # self.counter = self.counter + 1;

    
    # if next_target is not None:
    #   yield response.follow(next_target, self.parse)  
    pass
