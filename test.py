from flask import Flask
from datetime import datetime 

import statistics

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres2020@localhost:5431/finance'

with app.app_context():
    # DB
    from api_finance.models import db, Quotas, Action
    db.init_app(app)

    actions = []

    actions_db = Action.query().filter().all()
    for action in actions_db:
        action_info = dict(
            id=action.id,
            company_name=action.company_name,
            company_full_name=action.company_full_name,
            sector=action.sector,
            segment=action.segment
        )

        quotas = Quotas.query().filter(Quotas.action_id == action.id, Quotas.date >= datetime(2020,1,1)).order_by(Quotas.date.asc()).all()
        has_data_in_2021 = False
        for q in quotas[::-1]:
            if q.date >= datetime(2021,1,1):
                has_data_in_2021 = True
                break
        
        if has_data_in_2021:
            action_info['quotas'] = [
                dict(value=quota.price, date=quota.date, deleted_at=quota.deleted_at) \
                    for quota in quotas]

            actions.append(action_info)

    
    for a_indice in range(len(actions)):
        actions[a_indice]['pstdev'] = statistics.pstdev([q['value'] for q in actions[a_indice]['quotas']])

    print('ok')