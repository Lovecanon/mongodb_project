from pymongo import MongoClient
from bson import ObjectId
import requests
import json
import re

# p_url = 'http://music.163.com/api/playlist/detail?id=602266946'
# s_url = 'http://music.163.com/weapi/v1/resource/comments/R_AL_3_35157561/?csrf_token='
#
# data = {
#     'params': 'CBLdjiE9VGyoIIXDZknaIx1RTkQUckueXd2iihJMwJEI9hWUek1S3rrsZVFeeARUaD3bW3lRFWk5fvlNvzNWrJ7TgVGaiyWDyKcx7JQcRxNuOqYz5pce6daITH59SjT1',
#     'encSecKey': '82886d43fb2c2daae7941b1f6a4290fa92506b0817006d3c2516ce3aff5127b169cba1443809e429f38c3094a7b60c801fbf9079266237723f8046ee79ef0ebdf1d96be51ae60e16bf7b5a048d9c6b3e786bae2bddfd29b4bb7e365de1df1107e26777811a01e308763d528a8fccfd17a7a439541a8b66d801f17d38921e64e9'
# }
# headers = {
#     'Cookie': 'appver=1.5.0.75771',
#     'Referer': 'http://music.163.com',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
# }
#
# resp = requests.post(s_url, data=data, headers=headers)
# print(resp.text)

# Mongodb配置
client = MongoClient('127.0.0.1', 27017)
client['test'].authenticate("root", "root")
db = client['test']
collection = db.person

result = collection.update({'name': 'Jack'}, {'name': 'Jack', 'age': 23}, upsert=True)
print(result)


