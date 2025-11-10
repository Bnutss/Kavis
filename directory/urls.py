from django.urls import path
from .views import MusteriListView, MusteriCreateView, MusteriUpdateView, MusteriDeleteView

app_name = "directory"

urlpatterns = [
    path("musteriler/", MusteriListView.as_view(), name="musteri_listesi"),
    path("musteri/olustur/", MusteriCreateView.as_view(), name="musteri_olustur"),
    path("musteri/<int:pk>/guncelle/", MusteriUpdateView.as_view(), name="musteri_guncelle"),
    path("musteri/<int:pk>/sil/", MusteriDeleteView.as_view(), name="musteri_sil"),
]
