from __future__ import print_function

from pymongo import MongoClient

client = MongoClient("lisa.stuy.edu")
db = client.test
restaurants = db.restaurants


def restaurants_by_borough(borough):
    return restaurants.find(dict(borough=borough))


def restaurants_by_zipcode(zipcode):
    return restaurants.find(dict(zipcode=zipcode))


def restaurants_by_borough_and_zipcode(borough, zipcode):
    q = {"$and": [dict(borough=borough), dict(zipcode=zipcode)]}
    return restaurants.find(q)


map(print, restaurants_by_borough("Brooklyn"))
map(print, restaurants_by_borough_and_zipcode("Brooklyn", "11209"))
