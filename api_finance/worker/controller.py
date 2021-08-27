import json
from flask import request
from api_finance.utils.flask import APIResource
from werkzeug.exceptions import BadRequest

from api_finance.worker import ns
from api_finance.worker.business import WorkerBusiness
from api_finance.worker.validators import validate

api = ns


@api.route('/actions')
class ActionsController(APIResource):

    def post(self):
        """
        get and save actions by fundamentus
        """
        status = WorkerBusiness.get_and_save_actions()
        return {"status": status}

    def put(self):
        """
        update actions information by fundamentus
        """
        status = WorkerBusiness.update_actions_infos()
        return {"status": status}


@api.route('/indicators')
class IndicatorsController(APIResource):

    def post(self):
        """
        get and save indicators by fundamentus
        """
        status = WorkerBusiness.get_and_save_indicators()
        return {"status": status}

@api.route('/extract_balance')
class BalanceController(APIResource):

    def post(self):
        """
        get and save balance by zip (fundamentus)
        """
        status = WorkerBusiness.get_and_save_balance()
        return {"status": status}

@api.route('/balance_download')
class BalanceController(APIResource):

    def post(self):
        """
        download balance zips by fundamentus
        """
        data, status = validate(request.json, 'download_balance')
        if status is False:
            raise BadRequest(json.dumps(data))

        status = WorkerBusiness.download_balance_zip(**data)
        return {"status": status}

@api.route('/quota')
class QuotaController(APIResource):

    def post(self):
        """
        get and save quota by fundamentus
        """
        data, status = validate(request.json, 'quota')
        if status is False:
            raise BadRequest(json.dumps(data))

        status = WorkerBusiness.get_and_save_quota(**data)
        return {"status": status}

@api.route('/fix-indicators')
class QuotaController(APIResource):

    def get(self):
        """
        fix indicators - set not last indicators with deleted_at
        """
        status = WorkerBusiness.fix_indicators()
        return {"status": status}

@api.route('/fix-quotas')
class QuotaController(APIResource):

    def get(self):
        """
        fix quotas - set last quota with deleted_at is None
        """
        status = WorkerBusiness.fix_quotas()
        return {"status": status}
