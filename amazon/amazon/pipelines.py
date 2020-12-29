
import pymongo
class AmazonPipeline(object):
    def __init__(self):
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        db = self.conn['amazon']
        self.collection = db['amazon']

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item


