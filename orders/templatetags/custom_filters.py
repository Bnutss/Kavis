from django import template

register = template.Library()


@register.filter
def get_durum_class(durum):
    durum_classes = {
        'onay_bekliyor': 'warning',
        'onaylandi': 'info',
        'malzeme_satin_alma': 'secondary',
        'uretimde': 'primary',
        'print_tkac': 'dark',
        'boya': 'success',
        'aksesuar_montaji': 'secondary',
        'kalite_kontrol': 'warning',
        'paketleme': 'info',
        'teslime_gonderildi': 'primary',
        'teslim_edildi': 'success',
        'tamamlandi': 'success',
        'iade_pererabotka': 'danger',
        'iptal': 'danger',
    }
    return durum_classes.get(durum, 'secondary')
