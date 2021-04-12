from api.utils.flask import APIResource

from api import __version__
from api.status import ns

api = ns

@api.route('/')
class StatusController(APIResource):
    
    def get(self):
        """
        Returns application status
        """
        return {
            'version': __version__,
            'message': 'Running',
            'description': 'API - REST WITH PYTHON'
        }
        