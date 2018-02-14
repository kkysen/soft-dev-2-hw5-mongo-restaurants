from __future__ import print_function

from itertools import islice
from pprint import pprint

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database


class Restaurants(object):
    
    def __init__(self,
                 inet_address='lisa.stuy.edu',
                 db_name='test',
                 collection_name='restaurants'
                 ):
        # type: (str, str, str) -> None
        self.client = MongoClient(inet_address)  # type: MongoClient
        self.db = self.client[db_name]  # type: Database
        self.restaurants = self.db[collection_name]  # type: Collection
    
    def count(self):
        # type: () -> int
        return self.restaurants.count()
    
    def by_borough(self, borough):
        # type: (str) -> Cursor
        return self.restaurants.find({'borough': borough})
    
    def by_zipcode(self, zipcode):
        # type: (str) -> Cursor
        return self.restaurants.find({'address.zipcode': zipcode})
    
    def by_borough_and_zipcode(self, borough, zipcode):
        # type: (str, str) -> Cursor
        return self.restaurants.find({
            '$and': [
                {'borough': borough},
                {'address.zipcode': zipcode},
            ]
        })
    
    def by_zipcode_and_grade(self, zipcode, grade):
        # type: (str, str) -> Cursor
        return self.restaurants.find({
            '$and': [
                {'address.zipcode': zipcode},
                {'grades': {'$elemMatch': {'grade': grade}}},
            ]
        })
    
    def by_zipcode_and_score_less_than(self, zipcode, score):
        # type: (str, int) -> Cursor
        return self.restaurants.find({
            '$and': [
                {'address.zipcode': zipcode},
                {'grades': {'$elemMatch': {'score': {'$lt': score}}}},
            ]
        })
    
    def close(self):
        # type: () -> None
        self.client.close()
    
    def __enter__(self):
        # type: () -> Restaurants
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # type: () -> None
        self.close()


if __name__ == '__main__':
    restaurants = Restaurants()  # type: Restaurants
    print(restaurants.count())
    print()
    map(pprint,
        islice((restaurant['address'].get('zipcode', None) for restaurant in
                restaurants.by_borough("Brooklyn")), 0, 10))
    map(print, restaurants.by_borough('Brooklyn').limit(2))
    print()
    map(print, restaurants.by_zipcode('11215').limit(2))
    print()
    map(pprint, restaurants.by_borough_and_zipcode('Brooklyn', '11209').limit(2))
    restaurants.close()
