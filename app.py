from flask import Response, request
from typing import Any, Dict

from movies import Movies

movies = Movies()


def query():
    # type: () -> Response
    query = request.form['query']  # type: Dict[str, Any]
    for query_part in query:
        query_func = movies.__dict__.get(query_part, None)
        if query_func is None or not hasattr(query_func, 'is_query'):
            return Response(status=400, response='')
    for query_part in query:
        query_func = movies.__dict__[query_part]
        
        