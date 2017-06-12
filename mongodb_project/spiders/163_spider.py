# -*- coding:utf8 -*-
import scrapy
import re
import logging
import json
from scrapy.http import Request, FormRequest
from mongodb_project import MongoUtils

logger = logging.getLogger(__name__)


class MusicSpider(scrapy.Spider):
    name = "163_spider"
    allowed_domains = ["music.163.com"]
    start_urls = ['']

    # 163配置
    post_data = {
        'params': 'CBLdjiE9VGyoIIXDZknaIx1RTkQUckueXd2iihJMwJEI9hWUek1S3rrsZVFeeARUaD3bW3lRFWk5fvlNvzNWrJ7TgVGaiyWDyKcx7JQcRxNuOqYz5pce6daITH59SjT1',
        'encSecKey': '82886d43fb2c2daae7941b1f6a4290fa92506b0817006d3c2516ce3aff5127b169cba1443809e429f38c3094a7b60c801fbf9079266237723f8046ee79ef0ebdf1d96be51ae60e16bf7b5a048d9c6b3e786bae2bddfd29b4bb7e365de1df1107e26777811a01e308763d528a8fccfd17a7a439541a8b66d801f17d38921e64e9'
    }
    limit = 35  # 每种口味的单页歌单数量
    page_num = 1  # 每种口味要爬取几页歌单

    # 歌单id缓存，防止重复插入。除此还可以使用playlist_buffer、comment_buffer做缓存，然后insert_many
    playlist_id_buffer = []
    db = MongoUtils.MongoDB().db

    def start_requests(self):
        """start_requests方法【必须】返回一个可迭代对象，该对象包含了spider用于爬取的第一个Request"""
        return [Request('http://music.163.com/discover/playlist', callback=self.pre_get_playlist)]

    def pre_get_playlist(self, response):
        playlist_urls = response.xpath('//dd/a[@data-cat]/@href').extract()
        logger.info('Find %d kinds of music taste' % (len(playlist_urls)))
        for playlist_url in playlist_urls:
            for offset in range(0, self.page_num * self.limit, self.limit):
                full_url = response.urljoin(playlist_url) + '&order=hot&limit=35&offset=' + str(offset)
                logger.info('Getting playlist url:' + full_url)
                yield Request(full_url, callback=self.in_get_playlist)

    def in_get_playlist(self, response):
        playlist_url = 'http://music.163.com/api/playlist/detail?id='
        playlist_ids = response.xpath('//ul/li/div/div/a/@data-res-id').extract()
        for id in playlist_ids:
            if re.match('^\d{4,}\d$', id) and id not in self.playlist_id_buffer:
                self.playlist_id_buffer.append(id)
                yield Request(playlist_url + str(id), callback=self.post_get_playlist)

    def post_get_playlist(self, response):
        collection = self.db.playlist
        result = json.loads(response.body, encoding='utf-8')['result']

        # inserted = collection.update({'id': result['id']}, result, upsert=True)  # upsert=True表示insert or update
        # logger.info('Update or Insert to playlist database[%s]' % (str(inserted),))
        if result['id'] not in self.playlist_id_buffer:
            collection.insert(result)

        for song in result['tracks']:
            artists = []
            for detail in song['artists']:
                artists.append(detail['name'])
            comment_url = 'http://music.163.com/weapi/v1/resource/comments/%s/?csrf_token=' % (song['commentThreadId'],)
            # 使用FormRequest来进行POST登陆，或者使用下面的方式登陆
            # Request(url, method='POST', body=json.dumps(data))
            yield FormRequest(comment_url, formdata=self.post_data, callback=self.parse,
                              meta={'m_id': song['id'], 'm_name': song['name'], 'artists': artists})

    def parse(self, response):
        collection = self.db.comment
        comment_body = json.loads(response.body, encoding='utf-8')
        music_id = response.meta['m_id']
        comment_body['m_id'] = music_id
        comment_body['m_name'] = response.meta['m_name']
        comment_body['artists'] = response.meta['artists']
        collection.update({'id': music_id}, comment_body, upsert=True)
        # logger.info('Update or Insert to Mongodb[%s]' % (str(inserted),))
        yield
