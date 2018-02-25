from __future__ import print_function

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database


class Crimes(object):
    
    def __init__(self,
                 inet_address='lisa.stuy.edu',
                 db_name='mongols',
                 collection_name='crimes'
                 ):
        # type: (str, str, str) -> None
        self.client = MongoClient(inet_address)  # type: MongoClient
        self.db = self.client[db_name]  # type: Database
        self.restaurants = self.db[collection_name]  # type: Collection
    
    def count(self):
        # type: () -> int
        return self.restaurants.count()
    
    # TODO query methods
    
    def close(self):
        # type: () -> None
        self.client.close()
    
    def __enter__(self):
        # type: () -> Crimes
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # type: () -> None
        self.close()


if __name__ == '__main__':
    historicalEvent = Crimes()  # type: Crimes
    
    pprint = print
    if False:
        import pprint
        
        pprint = pprint.pprint
    
    # TODO tests
