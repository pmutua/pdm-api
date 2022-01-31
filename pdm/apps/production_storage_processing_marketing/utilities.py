from pdm.apps.production_storage_processing_marketing.models import Evoucher



def autogenerate_evoucher_no():
    """Autogenerate E-voucher no"""
    last_obj = Evoucher.objects.all().last()
    if last_obj is None:
        return 'ev-0'
    else:
        return f'ev-{last_obj.id+1}'

