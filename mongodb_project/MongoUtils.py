from pymongo import MongoClient
import sys
import logging

logger = logging.getLogger(__name__)

# 如果数据库设置可权限，就必须要填写username、password
MONGODB_CONFIG = {
    'host': '127.0.0.1',
    'port': 27117,
    'db': 'music',
    'username': None,
    'password': None
}


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class MongoDB(Singleton):
    def __init__(self):
        try:
            self.client = MongoClient(MONGODB_CONFIG['host'], MONGODB_CONFIG['port'])
            self.db = self.client[MONGODB_CONFIG['db']]
            # 如果给出用户名和密码进行验证
            if MONGODB_CONFIG['username'] and MONGODB_CONFIG['password']:
                self.db.authenticate(MONGODB_CONFIG['username'], MONGODB_CONFIG['password'])
        except Exception as e:
            logger.error(e)
            sys.exit(1)





