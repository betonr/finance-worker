"""
formatting the return of the salesman controllers
"""

from flask_restplus import fields

def get_salesman_serializer(username=True):
    schema = {
        "id": fields.String(),
        "name": fields.String(),
        "email": fields.String(),
        "created_at": fields.DateTime(),
        "status": fields.Boolean()
    }
    if username:
        schema['auth'] = fields.Nested({
            "username": fields.String()
        })
    return schema


def get_salesman_list_serializer():
    return {
        'salesman': fields.List(fields.Nested(get_salesman_serializer()))
    }


def get_paginate_serializer():
    return {
        'page': fields.Integer(description='Number of this page of results'),
        'pages': fields.Integer(description='Total number of pages of results'),
        'per_page': fields.Integer(description='Number of items per page of results'),
        'total': fields.Integer(description='Total number of results'),
        'items': fields.List(fields.Nested(get_salesman_serializer()))
    }
