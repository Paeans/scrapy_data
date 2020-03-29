# -*- coding: utf-8 -*-
import scrapy
import time


class AirbnbexSpider(scrapy.Spider):
  name = 'airbnbex'
  allowed_domains = ['www.airbnb.com']
  start_urls = ['https://www.airbnb.com/s/Houston--United-States/experiences']
  counter = 0

  def parse(self, response):
    for exps in response.css('div._1xl0u0x'):
      exps_url = exps.xpath('a/@href').get();
      yield {
          'exps_url': exps_url,
          'host_id': exps_url.split('/')[2].split('?')[0],
      }
    
    next_target = response.xpath('//a[@aria-label="Next page"]/@href').get();
    yield {
      'next target': next_target,
      'page index': self.counter,
    }
    
    self.counter = self.counter + 1;
    #next_page = response.css('li.next a::attr("href")').get()
    #yield {
    #      'author': "next page",
    #      'text': "1",
    #}
    time.sleep(2);
    if next_target is not None:
      yield response.follow(next_target, self.parse)  
    pass
