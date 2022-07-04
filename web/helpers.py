from flask import request
import json
from flask.json import dumps as json_dumps


def get_input(columns=None, request_data=None):
    """Retrieve speficied columns from request data. If the column is not available it wont be added to the returned dictionary.

    Args:
        columns (list, optional): Column keys you want to retrieve. Defaults to all columns.
        request_data (dict, optional): The entire request data. Defaults to request data from flask.

    Returns:
        dict: The resulting dictionary with only the needed columns that are not emtpy
    """
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
    """Parse a SQLAlchemy model to a dictionary

    Args:
        item (SQLAlechmyModel): The SQLAlchemyModel

    Returns:
        dict: The represented dict.
    """
    return json.loads(json_dumps(item))

def add_relationship(item, relationship):
    """Add specified raltionship to SQLAlchemy model and return the dictionary

    Args:
        item (SQLAlechmyModel): The model where a relationship needs to be added
        relationship (string): The relationship

    Returns:
        dict: The model including the added relationship.
    """
    relation = getattr(item, relationship)
    item = parse_model(item)
    item[relationship] = relation
    return item

def get_or_create(session, model, query, values = None):
    """Get model or create one if it does not exists according to the query

    Args:
        session (SQLAlchemySession): The current database session
        model (SQLAlchemyModel): The model which needs to be retrieved/created
        query (dict): The query to which to retrieve the model if exists
        values (dict, optional): The values when creating the model. Defaults to the query dictionary.

    Returns:
        SQLAlchemyModel: The retrieved or created model. 
    """
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
    """Update model or create one if it does not exists according to the query

    Args:
        session (SQLAlchemySession): The current database session
        model (SQLAlchemyModel): The model which needs to be retrieved/created
        query (dict): The query to which to retrieve the model if exists
        values (dict, optional): The values when creating the model. Defaults to the query dictionary.

    Returns:
        SQLAlchemyModel: The retrieved or created model. 
    """
    if values == None:
        values = query
    instance = session.query(model).filter_by(**query).first()
    if instance:
        session.query(model).filter_by(id=instance.id).update(values)
    else:
        instance = model(**values)
        session.add(instance)
    session.commit()
    return instance
