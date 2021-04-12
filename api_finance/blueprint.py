from flask import Blueprint
from flask_restplus import Api

from api.worker.controller import api as worker_ns
from api.status.controller import api as status_ns

bp = Blueprint('api', __name__, url_prefix='/api')

new_api = Api(bp, doc=False)

new_api.add_namespace(worker_ns)
new_api.add_namespace(status_ns)
