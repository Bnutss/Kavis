from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.db.models import Sum, Count
from directory.models import Musteri
from orders.models import Siparis
from django.utils import timezone
from datetime import timedelta


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'users/auth/login_page.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('users:dashboard')
            else:
                form.add_error(None, "Неправильное имя пользователя или пароль.")

        return render(request, 'users/auth/login_page.html', {'form': form})


class LogoutView(View):
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('users:login')

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('users:login')


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'mainmenu/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Основная статистика
        toplam_musteri = Musteri.objects.count()
        bekleyen_siparis = Siparis.objects.exclude(durum__in=['tamamlandi', 'iptal', 'teslim_edildi']).count()
        tamamlanan_siparis = Siparis.objects.filter(durum__in=['tamamlandi', 'teslim_edildi']).count()

        # Расчет общей выручки
        toplam_hasilat_data = Siparis.objects.filter(
            durum__in=['tamamlandi', 'teslim_edildi']
        ).aggregate(
            total=Sum('fiyat', field='fiyat * miktar')
        )['total'] or 0

        # Статистика за последние 30 дней
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        son_30_gun_hasilat = Siparis.objects.filter(
            durum__in=['tamamlandi', 'teslim_edildi'],
            siparis_tarihi__gte=thirty_days_ago
        ).aggregate(
            total=Sum('fiyat', field='fiyat * miktar')
        )['total'] or 0

        # Активные заказы (последние 7 дней)
        active_orders = Siparis.objects.filter(
            siparis_tarihi__gte=timezone.now().date() - timedelta(days=7)
        ).count()

        # Статистика по статусам
        durum_choices = dict(Siparis.DURUM_CHOICES)
        durum_istatistikleri = []
        kritik_durumlar = []

        for durum_key, durum_label in durum_choices.items():
            siparisler = Siparis.objects.filter(durum=durum_key)
            sayi = siparisler.count()
            toplam_tutar = siparisler.aggregate(
                total=Sum('fiyat', field='fiyat * miktar')
            )['total'] or 0

            durum_info = {
                'key': durum_key,
                'label': durum_label,
                'sayi': sayi,
                'toplam_tutar': toplam_tutar,
                'renk': self.get_durum_renk(durum_key),
                'icon': self.get_durum_icon(durum_key)
            }

            durum_istatistikleri.append(durum_info)

            # Критические статусы для верхних карточек
            if durum_key in ['onay_bekliyor', 'uretimde', 'kalite_kontrol']:
                kritik_durumlar.append(durum_info)

        # Последние заказы
        son_siparisler = Siparis.objects.select_related('musteri').order_by('-siparis_tarihi')[:5]

        context.update({
            'toplam_musteri': toplam_musteri,
            'bekleyen_siparis': bekleyen_siparis,
            'tamamlanan_siparis': tamamlanan_siparis,
            'toplam_hasilat': toplam_hasilat_data,
            'son_30_gun_hasilat': son_30_gun_hasilat,
            'active_orders': active_orders,
            'dashboard_stats': [
                {
                    'title': 'Toplam Müşteri',
                    'value': toplam_musteri,
                    'icon': 'bi-people',
                    'bg_color': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    'trend': '+12%'
                },
                {
                    'title': 'Aktif Siparişler',
                    'value': active_orders,
                    'icon': 'bi-clock',
                    'bg_color': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                    'trend': '+5%'
                },
                {
                    'title': 'Tamamlanan Sipariş',
                    'value': tamamlanan_siparis,
                    'icon': 'bi-check-circle',
                    'bg_color': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                    'trend': '+8%'
                },
                {
                    'title': 'Toplam Hasılat',
                    'value': toplam_hasilat_data,
                    'icon': 'bi-currency-dollar',
                    'bg_color': 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
                    'trend': '+15%',
                    'is_currency': True
                }
            ],
            'kritik_durumlar': kritik_durumlar[:3],
            'durum_istatistikleri': durum_istatistikleri,
            'son_siparisler': son_siparisler
        })
        return context

    def get_durum_renk(self, durum):
        renkler = {
            'onay_bekliyor': 'warning',
            'onaylandi': 'info',
            'malzeme_satin_alma': 'secondary',
            'uretimde': 'primary',
            'print_tkac': 'dark',
            'boya': 'success',
            'aksesuar_montaji': 'light',
            'kalite_kontrol': 'warning',
            'paketleme': 'info',
            'teslime_gonderildi': 'primary',
            'teslim_edildi': 'success',
            'tamamlandi': 'success',
            'iade_pererabotka': 'danger',
            'iptal': 'danger',
        }
        return renkler.get(durum, 'secondary')

    def get_durum_icon(self, durum):
        iconlar = {
            'onay_bekliyor': 'bi-hourglass-split',
            'onaylandi': 'bi-check-lg',
            'malzeme_satin_alma': 'bi-cart',
            'uretimde': 'bi-gear',
            'print_tkac': 'bi-printer',
            'boya': 'bi-brush',
            'aksesuar_montaji': 'bi-tools',
            'kalite_kontrol': 'bi-clipboard-check',
            'paketleme': 'bi-box',
            'teslime_gonderildi': 'bi-truck',
            'teslim_edildi': 'bi-house-check',
            'tamamlandi': 'bi-flag-fill',
            'iade_pererabotka': 'bi-arrow-return-left',
            'iptal': 'bi-x-circle',
        }
        return iconlar.get(durum, 'bi-circle')
