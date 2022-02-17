import json
import decimal
from pdm.apps.production_storage_processing_marketing.models import Evoucher


def autogenerate_evoucher_no():
    """Autogenerate E-voucher no"""
    last_obj = Evoucher.objects.all().last()
    if last_obj is None:
        return "ev-0"
    else:
        return f"ev-{last_obj.id+1}"


class DecimalEncoder(json.JSONEncoder):
    """Encodes Decimal objects"""

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)
