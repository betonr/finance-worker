from datetime import datetime

def get_info_by_table(table, index, type='str'):
    try:
        value = table[table.index('?{}'.format(index))+1]
        i = 1
        while value == '':
            i += 1
            value = table[table.index('?{}'.format(index))+i]
    except:
        value = '-'
        
    if type == 'int':
        return 0 if value.replace(' ','') == '-' else int(value.replace('%', '').replace('.', ''))
    elif type == 'float':
        return 0.0 if value.replace(' ','') == '-' else float(value.replace('%', '').replace('.', '').replace(',', '.'))
    elif type == 'date':
        return None if value == '-' else datetime.strptime(value, '%d/%m/%Y')
    else:
        return value