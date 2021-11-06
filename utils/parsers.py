from datetime import datetime

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def parse_datetime(timestamp):
    return datetime.strptime(timestamp, TIME_FORMAT)


class PaystackAuthorization(object):
    def __init__(self, payload):
        self.authorization_code = payload.get("authorization_code", None)
        self.bin = payload.get("bin", None)
        self.last_4 = payload.get("last4", None)
        self.exp_month = int(payload.get("exp_month", 1))
        self.exp_year = int(payload.get("exp_year", 1))
        self.card_type = payload.get("card_type", None)
        self.bank = payload.get("bank", None)
        self.country_code = payload.get("country_code", None)
        self.brand = payload.get("brand", None)
        self.account_name = payload.get("account_name", None)
