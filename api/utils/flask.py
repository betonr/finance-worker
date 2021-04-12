from flask import Response, json
from flask_restplus import Resource
from werkzeug.exceptions import HTTPException


def return_response(data, status_code, dumps=True):
    """Formats return for application / json."""
    data = json.dumps(data) if dumps else data
    return Response(data, status_code, content_type='application/json')


class APIResource(Resource):
    """API Resource.
    It aims to override `dispatch_request` member in order to
    handle status_code and error message through exception contexts.
    The exceptions must inherit from @APIError.
    """

    def dispatch_request(self, *args, **kwargs):
        """Override dispatch request to handle HTTP Errors.
        Args:
            args (tuple) - Flask API Resource Args
            kwargs (dict) - Flask API Resource Kwargs parameters
        Returns:
            Response HTTP Response object
        """
        try:
            return super().dispatch_request(*args, **kwargs)
        except HTTPException as e:
            return return_response({
                "code": e.code,
                "message": e.description
            }, e.code)
        except BaseException as e:
            return return_response({
                "code": 500,
                "message": str(e)
            }, 500)