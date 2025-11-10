from django.urls import path
from .views import (
    SiparisListView,
    SiparisCreateView,
    SiparisUpdateView,
    SiparisDeleteView,
    SiparisDurumGuncelleView
)

app_name = "orders"

urlpatterns = [
    path("siparisler/", SiparisListView.as_view(), name="siparis_listesi"),
    path("siparis/olustur/", SiparisCreateView.as_view(), name="siparis_olustur"),
    path("siparis/<int:pk>/guncelle/", SiparisUpdateView.as_view(), name="siparis_guncelle"),
    path("siparis/<int:pk>/sil/", SiparisDeleteView.as_view(), name="siparis_sil"),
    path("siparis/<int:pk>/durum-guncelle/", SiparisDurumGuncelleView.as_view(), name="siparis_durum_guncelle"),
]
