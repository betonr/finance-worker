from api_finance.utils.flask import APIResource

from api_finance import __version__
from api_finance.status import ns

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
        