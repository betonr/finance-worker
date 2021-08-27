from copy import deepcopy
from datetime import datetime, timedelta
from werkzeug.exceptions import (NotFound, Conflict)
from pathlib import Path
import tempfile
import zipfile
import pandas as pd

from api_finance.models import db, Action, Worker, Indicators, Balance, Quotas
from api_finance.utils.base_sql import BaseModel, db
from api_finance.utils.helpers import working_directory
from api_finance.worker.services import FundamentusServices

class WorkerBusiness():

    @classmethod
    def create_activity(cls):
        return Worker(
            start_datetime=datetime.now(),
            qnt_new_actions=0,
            qnt_update_quota=0,
            qnt_update_indicators=0,
            qnt_update_balance=0,
            actions_errors='',
            qnt_errors=0,
            obs=''
        )

    @classmethod
    def get_and_save_actions(cls):
        activity = cls.create_activity()

        actions_db = [act.id for act in Action.query().filter().all()]
        
        actions = FundamentusServices.get_actions()
        actions_full = []
        for action in actions:
            if action['id'] in actions_db:
                continue
            
            try:
                additional_infos = FundamentusServices.get_action_details(action['id'])
                activity.qnt_new_actions += 1
                actions_full.append(Action(**action, **additional_infos))

            except Exception as e:
                activity.actions_errors = '{},{}'.format(
                        activity.actions_errors, action['id'])
                activity.qnt_errors += 1
                activity.obs = str(e)[0:555]

        BaseModel.save_all(actions_full)
        activity.status = True
        activity.end_datetime = datetime.now()
        activity.save()
        return True

    @classmethod
    def update_actions_infos(cls):
        for action in Action.query().filter().all():
            try:
                if '?' in action.sector or '?' in action.segment:
                    additional_infos = FundamentusServices.get_action_details(action.id)

                    action.sector = additional_infos['sector'] if '?' not in additional_infos['sector'] else ''
                    action.segment = additional_infos['segment'] if '?' not in additional_infos['segment'] else ''
                    
                    db.session.commit()

            except Exception as e:
                pass
        return True

    @classmethod
    def get_and_save_indicators(cls):
        activity = cls.create_activity()

        new_indicators = []
        actions_db = Action.query().filter().all()
        indicators_db = Indicators.query().filter(Indicators.deleted_at==None).all()
        for action in actions_db:
            action_id = action.id
            try:
                indicators_by_action = FundamentusServices.get_indicators(action_id)
                update = True

                if indicators_by_action.get('date'):
                    # verify if exist in db and your date is equals
                    for indicator_db in indicators_db:
                        if indicator_db.action_id == action_id:
                            if(indicator_db.date == indicators_by_action['date']):
                                update = False
                                break
                            indicator_db.deleted_at = datetime.now()
                            db.session.commit()
                            break

                    if update:
                        activity.qnt_update_indicators += 1
                        new_indicators.append(Indicators(
                            action_id=action_id,
                            **indicators_by_action
                        ))

            except Exception as e:
                activity.actions_errors = '{},{}'.format(activity.actions_errors, action_id)
                activity.qnt_errors += 1
                activity.obs = str(e)[0:555]

        BaseModel.save_all(new_indicators)
        activity.status = True
        activity.end_datetime = datetime.now()
        activity.save()
        return True

    @classmethod
    def get_and_save_balance(cls):
        activity = cls.create_activity()

        new_balances = []
        actions_db = Action.query().filter().all()
        balances_db = Balance.query().filter().all()
        for action in actions_db:
            action_id = action.id

            # extract zip
            data_folder = 'balance_zips'
            tmp_dirname = tempfile.mkdtemp()

            try:

                zip_action = Path('{}/{}.zip'.format(data_folder, action_id))
                if zip_action.is_file():
                    zipfile.ZipFile(zip_action).extractall('{}/{}'.format(tmp_dirname, action_id))
                    xls_file = '{}/{}/balanco.xls'.format(tmp_dirname, action_id)

                    b_content = pd.read_excel(xls_file, sheet_name='Bal. Patrim.', index_col=None, header=None)[1:]
                    r_content = pd.read_excel(xls_file, sheet_name='Dem. Result.', index_col=None, header=None)[1:]
                    b_keys = b_content[0][1:]
                    r_keys = r_content[0][1:]
                    for c in b_content.columns[1:]:
                        date = datetime.strptime(b_content[c][1], '%d/%m/%Y')
                        # verify if exist in db
                        if len(list(filter(lambda x: x.action_id == action_id and x.date == date, balances_db))) > 0:
                            continue
                        
                        # balance sheet
                        balance = dict()
                        for i in range(2, (len(b_keys)+2)):
                            balance[b_keys[i]] = str(b_content[c][i])

                        # result sheet
                        result = dict()
                        for i in range(2, (len(r_keys)+2)):
                            result[r_keys[i]] = str(r_content[c][i])
                        
                        activity.qnt_update_balance += 1
                        new_balances.append(Balance(
                            action_id=action_id,
                            date=date,
                            total_assets=balance['Ativo Total'],
                            total_liabilities=balance['Passivo Total'],
                            net_worth=balance['Patrimônio Líquido'],
                            balance_infos=balance,
                            result_infos=result
                        ))
                else:
                    continue

            except Exception as e:
                activity.actions_errors = '{},{}'.format(activity.actions_errors, action_id)
                activity.qnt_errors += 1
                activity.obs = str(e)[0:555]

        BaseModel.save_all(new_balances)
        activity.status = True
        activity.end_datetime = datetime.now()
        activity.save()
        return True

    @classmethod
    def download_balance_zip(cls, session_id):
        actions_db = Action.query().filter().all()
        for action in actions_db:
            action_id = action.id
            try:
                content, status = FundamentusServices.get_hist_balance_zip(session_id, action_id)
                if status:
                    with open('balance_zips/{}.zip'.format(action_id), 'wb') as file:
                        file.write(content)
            except Exception as e:
                print(e)
                continue
        return True

    @classmethod
    def get_and_save_quota(cls, start_date, last_date, only_last_quota=False):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        last_date = datetime.strptime(last_date, '%Y-%m-%d')
        activity = cls.create_activity()

        # set all quotas with deleted_at = start_date
        quotas = Quotas.query().filter(Quotas.deleted_at == None).all()
        for quota in quotas:
            quota.deleted_at = start_date
        db.session.commit()

        actions_db = Action.query().filter().all()
        for action in actions_db:
            action_id = action.id
            try:
                historic_quota = FundamentusServices.get_hist_quota(action_id)
                quotas = []
                if historic_quota:
                    if only_last_quota:
                        historic_quota = historic_quota[-2:]

                    for quota in historic_quota:
                        date = (datetime.fromtimestamp(quota[0] / 1e3) + timedelta(hours=3)).replace(minute=0, hour=0, second=0)
                        if date >= start_date and date <= last_date:
                            quotas.append(Quotas(
                                action_id=action_id,
                                price=float(quota[1]),
                                date=date,
                                deleted_at=date + timedelta(days=1) if date != last_date else None
                            ))

                if len(quotas):
                    BaseModel.save_all(quotas)
                    activity.qnt_update_quota += 1

            except Exception as e:
                activity.actions_errors = '{},{}'.format(activity.actions_errors, action_id)
                activity.qnt_errors += 1
                activity.obs = str(e)[0:555]

        activity.status = True
        activity.end_datetime = datetime.now()
        activity.save()
        return True

    @classmethod
    def fix_indicators(cls,):
        actions_db = Action.query().filter().all()

        for action in actions_db:
            indicators = Indicators.query().filter(Indicators.action_id == action.id).order_by(Indicators.date.desc()).all()

            i = 0
            last_indicator = None

            for indicator in indicators:
                if i > 0:
                    indicator.deleted_at = last_indicator

                last_indicator = indicator.date
                i += 1

            db.session.commit()

        return True

    @classmethod
    def fix_quotas(cls,):
        actions_db = Action.query().filter().all()

        for action in actions_db:
            quotas = Quotas.query().filter(Quotas.action_id == action.id).order_by(Quotas.date.asc()).all()
    
            for quota in quotas:
                quota.deleted_at = None
                break

            db.session.commit()

        return True