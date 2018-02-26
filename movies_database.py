'''
Team Mongols Anish Shenoy and Khyber Sen
SoftDev2 pd07
K05 -- Import/Export Bank
2018-02-25

Name of Dataset: American movies scraped from Wikipedia
Description: A List of American Movies scraped from the popular online encyclopedia known as Wikipedia
Download: https://raw.githubusercontent.com/prust/wikipedia-movie-data/master/movies.json
Import Mechanism:
    Our import mechanism first reads the file using the "get_json()" function which reads the given filename
    and then uses the "json_util.loads()" function to return the file's data as python objects (in this case, a list of dictionaries).
    Next, our add_json function creates the database and collection (if it hasn't already been created)
    and then uses pymongo's "<collection_name>.insert_many()" to add the data to our databse.
'''

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database
from bson import json_util

#returns json file as list of dicts
def get_json(filename):
    f = open(filename)
    raw = f.read()
    data = json_util.loads(raw)
    print "got json data"
    return data

def add_json(connection, db_name, col_name, data):
    print "adding..."
    db = connection[db_name]
    col = db[col_name]
    col.insert_many(data)
    print "added json data"

if __name__ == '__main__':
    c = MongoClient("lisa.stuy.edu")
    data = get_json("movies.json")
    add_json(c, "mongols", "movies", data)
