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

        toplam_musteri = Musteri.objects.count()

        active_orders = Siparis.objects.filter(
            siparis_tarihi__gte=timezone.now().date() - timedelta(days=7)
        ).count()

        tamamlanan_siparis = Siparis.objects.filter(
            durum__in=['tamamlandi', 'teslim_edildi']
        ).count()

        toplam_hasilat = Siparis.objects.filter(
            durum__in=['tamamlandi', 'teslim_edildi']
        ).aggregate(
            total=Sum('fiyat', field='fiyat * miktar')
        )['total'] or 0

        musteri_istatistikleri = []
        musteriler = Musteri.objects.filter(aktif=True)

        for musteri in musteriler:
            siparisler = Siparis.objects.filter(musteri=musteri).order_by('-siparis_tarihi')

            toplam_siparis = siparisler.count()
            bekleyen = siparisler.exclude(durum__in=['tamamlandi', 'iptal', 'teslim_edildi']).count()
            tamamlanan = siparisler.filter(durum__in=['tamamlandi', 'teslim_edildi']).count()

            toplam_tutar = sum([s.get_toplam_tutar() for s in siparisler])
            tamamlanan_tutar = sum([
                s.get_toplam_tutar() for s in siparisler
                if s.durum in ['tamamlandi', 'teslim_edildi']
            ])

            son_siparis = siparisler.first()
            son_siparis_tarihi = son_siparis.siparis_tarihi if son_siparis else None

            if toplam_siparis > 0:
                musteri_istatistikleri.append({
                    'musteri': musteri,
                    'toplam_siparis': toplam_siparis,
                    'bekleyen_siparis': bekleyen,
                    'tamamlanan_siparis': tamamlanan,
                    'toplam_tutar': toplam_tutar,
                    'tamamlanan_tutar': tamamlanan_tutar,
                    'son_siparis_tarihi': son_siparis_tarihi,
                    'tamamlanma_orani': round((tamamlanan / toplam_siparis) * 100, 1),
                    'siparisler': list(siparisler)
                })

        musteri_istatistikleri.sort(key=lambda x: x['toplam_tutar'], reverse=True)

        context.update({
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
                    'value': toplam_hasilat,
                    'icon': 'bi-currency-dollar',
                    'bg_color': 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
                    'trend': '+15%',
                    'is_currency': True
                }
            ],
            'musteri_istatistikleri': musteri_istatistikleri
        })

        return context
