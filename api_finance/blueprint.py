from flask import Blueprint
from flask_restplus import Api

from api_finance.worker.controller import api as worker_ns
from api_finance.status.controller import api as status_ns

bp = Blueprint('api', __name__, url_prefix='/api')

new_api_finance = Api(bp, doc=False)

new_api_finance.add_namespace(worker_ns)
new_api_finance.add_namespace(status_ns)
