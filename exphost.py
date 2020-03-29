# -*- coding: utf-8 -*-
import scrapy
import time

import json


class ExpHostSpider(scrapy.Spider):
  name = 'airbnbex'
  allowed_domains = ['www.airbnb.com']
  id_list = [] # 513872, 363792
  id_index = 0
  offset = 0
  
  def start_requests(self):
    with open('uniq_id.txt', 'r') as id_file:
      for line in id_file:
        self.id_list.append(line.strip())
    yield scrapy.Request(url='https://www.airbnb.com' + self.nextTarget(), callback=self.parse)

  def getReviesCount(self, res_text):
    data = json.loads(res_text)
    # res_data = json.loads(data['res'])
    return data['metadata']['reviews_count']

  def nextTarget(self):
    return '/api/v2/reviews?currency=USD&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&public=true&reviewable_id='+str(self.id_list[self.id_index])+'&reviewable_type=MtTemplate&role=guest&_limit=100&_offset='+ str(self.offset) +'&_format=for_experiences_guest_flow&supported_media_item_types%5B%5D=picture'

  def parse(self, response):
    res_text = response.text
    yield { 'host_id': self.id_list[self.id_index],
          'res': res_text, }

    self.offset = self.offset + 100;
    if self.offset >= self.getReviesCount(res_text):
      self.id_index = self.id_index + 1;
      self.offset = 0;
    if self.id_index < len(self.id_list):
      yield response.follow(self.nextTarget(), self.parse)

    pass
