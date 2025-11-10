from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Musteri


class MusteriListView(LoginRequiredMixin, ListView):
    model = Musteri
    template_name = "directory/musteri_listesi.html"
    context_object_name = "musteriler"


class MusteriCreateView(LoginRequiredMixin, CreateView):
    model = Musteri
    fields = ["ad", "ulke", "eposta", "aktif"]
    success_url = reverse_lazy("directory:musteri_listesi")


class MusteriUpdateView(LoginRequiredMixin, UpdateView):
    model = Musteri
    fields = ["ad", "ulke", "eposta", "aktif"]
    success_url = reverse_lazy("directory:musteri_listesi")


class MusteriDeleteView(LoginRequiredMixin, DeleteView):
    model = Musteri
    success_url = reverse_lazy("directory:musteri_listesi")
