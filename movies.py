"""
Team Mongols: Anish Shenoy and Khyber Sen
SoftDev2 pd07
K05 -- Import/Export Bank
2018-02-25

Name of Dataset: American movies scraped from Wikipedia
Description: A List of American Movies scraped from the popular online encyclopedia known as Wikipedia
Download: https://raw.githubusercontent.com/prust/wikipedia-movie-data/master/movies.json

Import Mechanism:
    Our import mechanism first reads the file in `Movies.import_json_file()`
    using `bson.json_util.loads()`, which returns the JSON in the file as a BSON Python object.
    `Movies.import_bson()` then inserts the BSON data into the collection,
    which was created in `Movies.__init__()`, using `pymongo.Collection.insert_many()`,
"""

from __future__ import print_function

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database
from typing import List, Dict, Any

from bson import json_util


class Movies(object):
    
    def __init__(self,
                 inet_address='lisa.stuy.edu',
                 db_name='mongols',
                 collection_name='movies'
                 ):
        # type: (str, str, str) -> None
        self.client = MongoClient(inet_address)  # type: MongoClient
        self.db = self.client[db_name]  # type: Database
        self.movies = self.db[collection_name]  # type: Collection
        self.query = []  # type: List[Dict[str, Any]]
        
    def count(self):
        # type: () -> int
        return self.movies.count()
    
    def import_bson(self, data):
        # type: (List[Dict[str, Any]]) -> None
        self.movies.insert_many(data)
    
    def import_json_file(self, filename='movies.json'):
        # type: (str) -> None
        with open(filename) as f:
            self.import_bson(json_util.loads(f.read()))
    
    def fetch(self):
        # type: () -> Cursor
        if len(self.query) == 0:
            query = {}
        else:
            query = {"$and": self.query}
        return self.movies.find(query)
    
    # query methods (chainable, will combine with $and)
    
    def with_title(self, title):
        # type: (str) -> Movies
        self.query.append({"title": title})
        return self
    
    def with_notes(self, notes):
        # type: (str) -> Movies
        self.query.append({"notes": notes})
        return self
    
    def by_director(self, director):
        # type: (str) -> Movies
        self.query.append({"director": director})
        return self
    
    def with_cast(self, cast):
        # type: (str) -> Movies
        self.query.append({"cast": cast})
        return self
    
    def in_genre(self, genre):
        # type: (str) -> Movies
        self.query.append({"genre": genre})
        return self
    
    def in_years(self, start_year, end_year):
        # type: (int, int) -> Movies
        self.query.append({"year": {
            "$gte": start_year,
            "$lte": end_year,
        }})
        return self
    
    def close(self):
        # type: () -> None
        self.client.close()
    
    def __enter__(self):
        # type: () -> Movies
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # type: () -> None
        self.close()


if __name__ == '__main__':
    movies = Movies()  # type: Movies
    
    init = False
    if init:
        movies.import_json_file()
    
    pprint = print
    if False:
        import pprint
        
        pprint = pprint.pprint

    pprint("***NUMBER OF MOVIES***")
    pprint(movies.count())
    pprint()

    # director
    print("***"
          "MOVIES BY DIRECTOR 'D. W. Griffith' "
          "***\n")
    map(pprint, movies
        .by_director('D. W. Griffith')
        .fetch()
        )
    print('\n')

    # director and cast
    print("***"
          "MOVIES BY DIRECTOR 'D. W. Griffith' "
          "AND WITH CAST 'Mack Sennett' "
          "***\n")
    map(pprint, movies
        .by_director('D. W. Griffith')
        .with_cast('Mack Sennett')
        .fetch()
        )
    print('\n')

    # director and cast and title
    print("***"
          "MOVIES BY DIRECTOR 'D. W. Griffith' "
          "AND WITH CAST 'Mack Sennett' "
          "AND WITH TITLE 'Those Awful Hats' "
          "***\n")
    map(pprint, movies
        .by_director('D. W. Griffith')
        .with_cast('Mack Sennett')
        .with_title('Those Awful Hats')
        .fetch()
        )
    print('\n')
    
    movies.close()
