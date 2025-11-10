from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.views import View
from .models import Siparis, Urun
from directory.models import Musteri


class SiparisListView(LoginRequiredMixin, ListView):
    model = Siparis
    template_name = "orders/siparis_listesi.html"
    context_object_name = "siparisler"

    def get_queryset(self):
        return Siparis.objects.select_related('musteri', 'urun').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['musteriler'] = Musteri.objects.filter(aktif=True)
        context['urunler'] = Urun.objects.all()
        return context


class SiparisCreateView(LoginRequiredMixin, CreateView):
    model = Siparis
    fields = ["siparis_no", "musteri", "urun", "urun_cinsi", "miktar", "fiyat", "siparis_tarihi", "uretici",
              "sevk_tarihi", "durum", "not_bilgisi"]
    success_url = reverse_lazy("orders:siparis_listesi")

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({'success': True, 'id': self.object.id})


class SiparisUpdateView(LoginRequiredMixin, UpdateView):
    model = Siparis
    fields = ["siparis_no", "musteri", "urun", "urun_cinsi", "miktar", "fiyat", "siparis_tarihi", "uretici",
              "sevk_tarihi", "durum", "not_bilgisi"]
    success_url = reverse_lazy("orders:siparis_listesi")

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({'success': True, 'id': self.object.id})


class SiparisDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        try:
            siparis = Siparis.objects.get(pk=pk)
            siparis.delete()
            return JsonResponse({'success': True})
        except Siparis.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Sipariş bulunamadı'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


class SiparisDurumGuncelleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        try:
            siparis = Siparis.objects.get(pk=pk)
            yeni_durum = request.POST.get('durum')

            if not yeni_durum:
                return JsonResponse({'success': False, 'error': 'Durum parametresi eksik'}, status=400)

            durum_values = [choice[0] for choice in Siparis.DURUM_CHOICES]
            if yeni_durum in durum_values:
                siparis.durum = yeni_durum
                siparis.save()
                return JsonResponse({'success': True})

            return JsonResponse({'success': False, 'error': 'Geçersiz durum'}, status=400)
        except Siparis.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Sipariş bulunamadı'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


class UrunFiyatGetirView(LoginRequiredMixin, View):
    def get(self, request, pk):
        try:
            urun = Urun.objects.get(pk=pk)
            return JsonResponse({
                'success': True,
                'fiyat': float(urun.fiyat),
                'ad': urun.ad
            })
        except Urun.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Ürün bulunamadı'}, status=404)
