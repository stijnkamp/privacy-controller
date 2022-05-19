from flask import request
import json
from flask.json import dumps as json_dumps


def get_input(columns=None, request_data=None):
    if request_data == None:
        request_data = request.json 
    data = {}
    if columns == None:
        return request_data
    for column in columns:
        if column in request_data:
            data[column] = request_data[column]
    return data


def parse_model(item):
    return json.loads(json_dumps(item))

def add_relationship(item, relationship):
    relation = getattr(item, relationship)
    item = parse_model(item)
    item[relationship] = relation
    return item

def get_or_create(session, model, query, values = None):
    if values == None:
        values = query
    instance = session.query(model).filter_by(**query).first()
    if instance:
        return instance
    else:
        instance = model(**values)
        session.add(instance)
        session.commit()
        return instance
def update_or_create(session, model, query, values = None):
    if values == None:
        values = query
    instance = session.query(model).filter_by(**query).first()
    if instance:
        instance.update(**values)
    else:
        instance = model(**values)
        session.add(instance)
    session.commit()
    return instance
