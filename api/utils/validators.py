from datetime import datetime

def to_date(s):
    return datetime.strptime(s, '%Y-%m-%d') if s else None