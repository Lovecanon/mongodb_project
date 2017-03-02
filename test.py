

class Person(object):
    def __init__(self, auth_encoding='latin-1'):
        self.auth_encoding = auth_encoding

    @classmethod
    def from_crawler(cls, auth_encoding):
        return cls(auth_encoding)

p = Person.from_crawler('utf-8')  # 并非简单的用Person()来创建一个新对象
print(p.auth_encoding)