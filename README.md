# 网易云音乐评论爬虫(Scrapy+MongoDB)

## 启动流程
1. 打开Mongodb服务器， 如果没有权限验证请关闭`--auth`和`MongoUtils`配置中的`username`、`password`
```bash
C:\Users\liaoxiangkai>mongod --dbpath "D://Program Files/MongoDB/data" --auth
```
1. 启动爬虫，`settings.py`文件中设置`DEFAULT_REQUEST_HEADERS`，其他的中间件、管道根据需求
```bash
D:\papp\mongodb_project>scrapy crawl 163_spider
```
1. 打开Mongodb的shell，默认端口27017
```bash
C:\Users\liaoxiangkai>mongo
> db.playlist.find().count()
32
> db.comment.find().count()
1228
```

## 爬取流程
`start_requests()`方法获取不同口味的链接，如：国语、欧美、古典等；

`pre_get_playlist()`访问每种口味链接下的歌单，同时限制了访问页数(limit、offset)；

`in_get_playlist()`获取每种口味下歌单页面信息，抽取歌单ids`playlist_ids`，再根据歌单id访问歌单API；

`post_get_playlist()`，在歌单API中找到此歌单包含的所有音乐id、名字、艺人`meta={'m_id': song['id'],'m_name': song['name'], 'artists': artists}`
 ，再访问评论API；

`parse()`获取评论的json数据后，添加音乐id、名字、艺人信息，之后将其保存到数据库。

----------------------------------

## 只是测试，跑了一分钟

```bash
> db.comment.find({}, {"_id": 0, "total": 1, "m_name": 1, "artists": 1}).sort({"total": -1}).limit(20)
{ "total" : 113477, "m_name" : "Five Hundred Miles", "artists" : [ "Justin Timberlake", "Carey Mulligan", "Stark Sands" ] }
{ "total" : 100634, "m_name" : "IF YOU", "artists" : [ "BIGBANG" ] }
{ "total" : 73229, "m_name" : "岁月神偷", "artists" : [ "金玟岐" ] }
{ "total" : 61191, "m_name" : "Schnappi", "artists" : [ "Joy Gruttmann" ] }
{ "total" : 51862, "m_name" : "The Phoenix", "artists" : [ "Fall Out Boy" ] }
{ "total" : 50148, "m_name" : "遇见", "artists" : [ "孙燕姿" ] }
{ "total" : 47620, "m_name" : "A Little Story", "artists" : [ "Valentin" ] }
{ "total" : 47329, "m_name" : "Sugar", "artists" : [ "Maroon 5" ] }
{ "total" : 43284, "m_name" : "Viva La Vida", "artists" : [ "Coldplay" ] }
{ "total" : 41417, "m_name" : "Croatian Rhapsody", "artists" : [ "马克西姆.姆尔维察" ] }
{ "total" : 38310, "m_name" : "Lost Stars", "artists" : [ "Adam Levine" ] }
{ "total" : 37951, "m_name" : "Valder Fields", "artists" : [ "Tamas Wells" ] }
{ "total" : 37897, "m_name" : "Closer", "artists" : [ "The Chainsmokers", "Halsey" ] }
{ "total" : 34152, "m_name" : "Tassel", "artists" : [ "Cymophane" ] }
{ "total" : 33994, "m_name" : "Love Yourself", "artists" : [ "Justin Bieber" ] }
{ "total" : 32592, "m_name" : "Summer Vibe", "artists" : [ "Walk off the Earth" ] }
{ "total" : 31808, "m_name" : "NEXT TO YOU", "artists" : [ "Ken Arai" ] }
{ "total" : 30779, "m_name" : "Bye Bye Bye", "artists" : [ "Lovestoned" ] }
{ "total" : 27903, "m_name" : "PRICKED (MINO & TAEHYUN)", "artists" : [ "WINNER" ] }
{ "total" : 27456, "m_name" : "HOLUP!", "artists" : [ "Bobby" ] }
```
--------------------------------------

## 这里是跑了几个小时的结果，可惜不带歌手信息(2017/3/2)

```bash
{ "total" : 1278759, "id" : 186016, "m_name" : "晴天" }
{ "total" : 664915, "id" : 411214279, "m_name" : "雅俗共赏" }
{ "total" : 234160, "id" : 418603077, "m_name" : "告白气球" }
{ "total" : 206226, "id" : 436514312, "m_name" : "成都" }
{ "total" : 176112, "id" : 412902689, "m_name" : "初学者" }
{ "total" : 169683, "id" : 32507038, "m_name" : "演员" }
{ "total" : 136540, "id" : 139774, "m_name" : "The truth that you leave" }
{ "total" : 133762, "id" : 417859631, "m_name" : "我好像在哪见过你" }
{ "total" : 131923, "id" : 443277013, "m_name" : "火星人来过" }
{ "total" : 118533, "id" : 31445772, "m_name" : "理想三旬" }
{ "total" : 118393, "id" : 439915614, "m_name" : "刚好遇见你" }
{ "total" : 113379, "id" : 27759600, "m_name" : "Five Hundred Miles" }
{ "total" : 110830, "id" : 412902950, "m_name" : "最佳歌手" }
{ "total" : 108745, "id" : 186001, "m_name" : "七里香" }
{ "total" : 106381, "id" : 2526613, "m_name" : "Booty Music" }
{ "total" : 104987, "id" : 417833348, "m_name" : "超越无限" }
{ "total" : 101300, "id" : 33211676, "m_name" : "Hello" }
{ "total" : 100584, "id" : 32922450, "m_name" : "IF YOU" }
{ "total" : 99476, "id" : 415792881, "m_name" : "刚刚好" }
{ "total" : 98114, "id" : 30953009, "m_name" : "See You Again" }
```