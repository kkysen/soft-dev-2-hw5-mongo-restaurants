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

    def by_less_than_grade(self, grade):
        #Check for GTE bc letters further down the alphabet (worse scores) have a higher value
        return self.restaurants.find({'grades': {'$elemMatch' : {'grade': {'$gte': grade}}}})

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
    print("***NUMBER OF RESTAURANTS***")
    print(restaurants.count())
    print()
    print("***RESTAURANTS IN BROOKLYN (5)***")
    map(print, restaurants.by_borough('Brooklyn').limit(5))
    print()
    print("***RESTAURANTS IN QUEENS (5)***")
    map(print, restaurants.by_borough('Queens').limit(5))
    print()
    print("***RESTAURANTS IN 11215 (5)***")
    map(print, restaurants.by_zipcode('11215').limit(5))
    print()
    print("***RESTAURANTS IN 11372 (5)***")
    map(print, restaurants.by_zipcode('11372').limit(5))
    print()
    print("***RESTAURANTS IN Brooklyn AND 11209 (5)***")
    map(pprint, restaurants.by_borough_and_zipcode('Brooklyn', '11209').limit(5))
    print()
    print("***RESTAURANTS IN Manhattan AND 10282 (5)***")
    map(pprint, restaurants.by_borough_and_zipcode('Manhattan', '10282').limit(5))
    print()
    print("***RESTAURANTS WITH A GRADE LESS THAN OR EQUAL TO 'B' (5)***")
    map(pprint, restaurants.by_less_than_grade("B").limit(5))
    print()
    print("***RESTAURANTS WITH A GRADE LESS THAN OR EQUAL TO 'C' (5)***")
    map(pprint, restaurants.by_less_than_grade("C").limit(5))
    print()
    restaurants.close()
