# 网易云音乐评论爬虫(Scrapy+MongoDB)

`start_requests()`方法获取不同口味的链接，如：国语、欧美、古典等；

`pre_get_playlist()`访问每种口味链接下的歌单，同时限制了访问页数(limit、offset)；

`in_get_playlist()`获取每种口味下歌单页面信息，抽取歌单ids`playlist_ids`，再根据歌单id访问歌单API；

`post_get_playlist()`，在歌单API中找到此歌单包含的所有音乐id、名字、艺人`meta={'m_id': song['id'],'m_name': song['name'], 'artists': artists}`
 ，再访问评论API；

`parse()`获取评论的json数据后，添加音乐id、名字、艺人信息，之后将其保存到数据库。