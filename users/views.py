from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.db.models import Sum
from directory.models import Musteri
from orders.models import Siparis


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
    template_name = 'mainmenu/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        toplam_musteri = Musteri.objects.count()
        bekleyen_siparis = Siparis.objects.exclude(durum='tamamlandi').count()
        tamamlanan_siparis = Siparis.objects.filter(durum='tamamlandi').count()
        toplam_hasilat_data = Siparis.objects.filter(durum='tamamlandi').aggregate(
            total=Sum('fiyat', field='fiyat * miktar')
        )['total']

        toplam_hasilat = toplam_hasilat_data if toplam_hasilat_data is not None else 0

        context['dashboard_stats'] = [
            {
                'title': 'Toplam Müşteri',
                'value': toplam_musteri,
                'icon_class': 'iconly-boldProfile',
                'bg_color': 'blue'
            },
            {
                'title': 'Bekleyen Sipariş',
                'value': bekleyen_siparis,
                'icon_class': 'iconly-boldTime-Square',
                'bg_color': 'orange'
            },
            {
                'title': 'Tamamlanan Sipariş',
                'value': tamamlanan_siparis,
                'icon_class': 'iconly-boldTick-Square',
                'bg_color': 'green'
            },
            {
                'title': 'Toplam Hasılat',
                'value': toplam_hasilat,
                'icon_class': 'iconly-boldChart',
                'bg_color': 'purple',
                'is_currency': True
            }
        ]
        return context
