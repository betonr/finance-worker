import os
import re
import json
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

from api_finance.config import Config
from api_finance.utils.worker import get_info_by_table

class FundamentusServices():

    @classmethod
    def get_actions(cls):
        # create session and set cookies
        session = requests.session()
        my_cookies = {'PHPSESSID': Config.session_id }
        requests.utils.add_dict_to_cookiejar(session.cookies, my_cookies)
        my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'}
        session.headers.update(my_headers)

        url_details = '{}/detalhes.php?papel='.format(Config.URL_PROVIDER_FUNDAMENTUS)
        r = session.get(url_details)
        html_soup = BeautifulSoup(r.text, 'html.parser')

        actions_html = html_soup.find_all('table', id='test1')[0].tbody
        actions_list = []
        for action in actions_html.contents:
            if action != '\n':
                infos = action.text.lstrip().split('\n')
                name = infos[0].replace('_', '')
                actions_list.append(dict(
                    id=name,
                    company_name=infos[1],
                    company_full_name=infos[2],
                    provider='fundamentus'
                ))
        return actions_list

    @classmethod
    def get_action_details(cls, id):
        # create session and set cookies
        session = requests.session()
        my_cookies = {'PHPSESSID': Config.session_id }
        requests.utils.add_dict_to_cookiejar(session.cookies, my_cookies)
        my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'}
        session.headers.update(my_headers)

        url_details = '{}/detalhes.php?papel={}'.format(Config.URL_PROVIDER_FUNDAMENTUS, id)
        r = session.get(url_details)
        html_soup = BeautifulSoup(r.text, 'html.parser')

        tables_html = html_soup.find_all('table', class_='w728')
        first_table = tables_html[0].text.split('\n')
        if not tables_html:
            return {}, False

        infos = dict(
            sector=get_info_by_table(first_table, 'Setor'),
            segment= get_info_by_table(first_table, 'Subsetor')
        )
        return infos

    @classmethod
    def get_indicators(cls, action_id):
        # create session and set cookies
        session = requests.session()
        my_cookies = {'PHPSESSID': Config.session_id }
        requests.utils.add_dict_to_cookiejar(session.cookies, my_cookies)
        my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'}
        session.headers.update(my_headers)

        url_details = '{}/detalhes.php?papel={}'.format(Config.URL_PROVIDER_FUNDAMENTUS, action_id)
        r = session.get(url_details)
        html_soup = BeautifulSoup(r.text, 'html.parser')

        tables_html = html_soup.find_all('table', class_='w728')
        first_table = tables_html[0].text.split('\n')
        third_table = tables_html[2].text.split('\n')
        if not tables_html:
            return {}, False

        infos = dict(
            date=get_info_by_table(first_table, 'Data últ cot', 'date'),
            price_profit=get_info_by_table(third_table, 'P/L', 'float'),
            price_value_worth=get_info_by_table(third_table, 'P/VP', 'float'),
            price_ebit=get_info_by_table(third_table, 'P/EBIT', 'float'),
            price_net_revenueear=get_info_by_table(third_table, 'PSR', 'float'),
            price_active=get_info_by_table(third_table, 'P/Ativos', 'float'),
            price_working_capital=get_info_by_table(third_table, 'P/Cap. Giro', 'float'),
            price_net_circle_active=get_info_by_table(third_table, 'P/Ativ Circ Liq', 'float'),
            div_yield=get_info_by_table(third_table, 'Div. Yield', 'float'),
            enterprise_value_ebitda=get_info_by_table(third_table, 'EV / EBITDA', 'float'),
            enterprise_value_ebit=get_info_by_table(third_table, 'EV / EBIT', 'float'),
            revenue_growth_five_years=get_info_by_table(third_table, 'Cres. Rec (5a)', 'float'),
            profit_by_action=get_info_by_table(third_table, 'LPA', 'float'),
            patrimonial_value=get_info_by_table(third_table, 'VPA', 'float'),
            gross_margin=get_info_by_table(third_table, 'Marg. Bruta', 'float'),
            ebit_margin=get_info_by_table(third_table, 'Marg. EBIT', 'float'),
            net_margin=get_info_by_table(third_table, 'Marg. Líquida', 'float'),
            ebit_active=get_info_by_table(third_table, 'EBIT / Ativo', 'float'),
            roic=get_info_by_table(third_table, 'ROIC', 'float'),
            roe=get_info_by_table(third_table, 'ROE', 'float'),
            current_assets_liabilities=get_info_by_table(third_table, 'Liquidez Corr', 'float'),
            debt_gross_patrimonial=get_info_by_table(third_table, 'Div Br/ Patrim', 'float'),
            asset_turnover=get_info_by_table(third_table, 'Giro Ativos', 'float')
        )
        return infos

    @classmethod
    def get_balance_by_site(cls, action_id):
        # create session and set cookies
        session = requests.session()
        my_cookies = {'PHPSESSID': Config.session_id }
        requests.utils.add_dict_to_cookiejar(session.cookies, my_cookies)
        my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'}
        session.headers.update(my_headers)

        url_details = '{}/detalhes.php?papel={}'.format(Config.URL_PROVIDER_FUNDAMENTUS, action_id)
        r = session.get(url_details)
        html_soup = BeautifulSoup(r.text, 'html.parser')

        tables_html = html_soup.find_all('table', class_='w728')
        second_table = tables_html[1].text.split('\n')
        fourth_table = tables_html[3].text.split('\n')
        if not tables_html:
            return {}, False

        infos = dict(
            date=get_info_by_table(second_table, 'Últ balanço processado', 'date'),
            market_value=get_info_by_table(second_table, 'Valor de mercado', 'int'),
            company_value=get_info_by_table(second_table, 'Valor da firma', 'int'),
            num_action=get_info_by_table(second_table, 'Nro. Ações', 'int'),
            assets=get_info_by_table(fourth_table, 'Ativo', 'int'),
            current_assets=get_info_by_table(fourth_table, 'Ativo Circulante', 'int'),
            availability=get_info_by_table(fourth_table, 'Disponibilidades', 'int'),
            gross_debt=get_info_by_table(fourth_table, 'Dív. Bruta', 'int'),
            net_debt=get_info_by_table(fourth_table, 'Dív. Líquida', 'int'),
            net_worth=get_info_by_table(fourth_table, 'Patrim. Líq', 'int')
        )
        return infos

    @classmethod
    def get_hist_balance_zip(cls, action_id):
        # create session and set cookies
        session = requests.session()
        my_cookies = {'PHPSESSID': Config.session_id }
        requests.utils.add_dict_to_cookiejar(session.cookies, my_cookies)
        my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'}
        session.headers.update(my_headers)

        # search action and save in session
        url_balance = '{}/balancos.php?papel={}&tipo=1'.format(Config.URL_PROVIDER_FUNDAMENTUS, action_id)
        session.get(url_balance)

        # download zip
        url_download = '{}/planilhas.php?SID={}'.format(Config.URL_PROVIDER_FUNDAMENTUS, session_id)
        r = requests.get(url_download)
        if r.status_code >= 300:
            return None, False
        return r.content, True
        
    @classmethod
    def get_hist_quota(cls, action_id):
        action_id = action_id.strip()
        # create session and set cookies
        session = requests.session()
        my_cookies = {'PHPSESSID': Config.session_id }
        requests.utils.add_dict_to_cookiejar(session.cookies, my_cookies)
        my_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'Host': 'www.fundamentus.com.br',
            'Referer': f'https://www.fundamentus.com.br/cotacoes.php?papel={action_id}'
        }
        session.headers.update(my_headers)

        url_quotas = f'{Config.URL_PROVIDER_FUNDAMENTUS}/amline/cot_hist.php?papel='
        r = session.get(f'{url_quotas}{action_id}')
        if r.status_code >= 300:
            return None
        return json.loads(r.text)
