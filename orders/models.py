from django.db import models
from directory.models import Musteri


class Siparis(models.Model):
    DURUM_CHOICES = [
        ('hazir', 'Hazır, Sevkiyat Bekliyor'),
        ('sevkiyatta', 'Sevkiyatta'),
        ('tamamlandi', 'Tamamlandı'),
        ('uretiliyor', 'Üretiliyor'),
        ('onay_bekliyor', 'Onay Bekliyor'),
        ('onaylandi', 'Onaylandı'),
        ('malzeme_satin_alma', 'Malzeme Satın Alma'),
        ('uretimde', 'Üretimde'),
        ('print_tkac', 'Baskı/Tkacılık'),
        ('boya', 'Boya'),
        ('aksesuar_montaji', 'Aksesuar Montajı'),
        ('kalite_kontrol', 'Kalite Kontrol'),
        ('paketleme', 'Paketleme'),
        ('teslime_gonderildi', 'Teslime Gönderildi'),
        ('teslim_edildi', 'Teslim Edildi'),
        ('iade_pererabotka', 'İade/Perak'),
        ('iptal', 'İptal'),
    ]

    siparis_no = models.CharField(max_length=50, unique=True, verbose_name="Sipariş No")
    musteri = models.ForeignKey(Musteri, on_delete=models.CASCADE, verbose_name="Müşteri")
    urun_cinsi = models.CharField(max_length=255, verbose_name="Ürün Cinsi")
    miktar = models.IntegerField(verbose_name="Miktar")
    fiyat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Fiyat")
    siparis_tarihi = models.DateField(verbose_name="Sipariş Tarihi")
    uretici = models.CharField(max_length=255, verbose_name="Üretici")
    sevk_tarihi = models.DateField(null=True, blank=True, verbose_name="Sevk Tarihi")
    durum = models.CharField(max_length=30, choices=DURUM_CHOICES, default='uretiliyor', verbose_name="Sipariş Durumu")
    not_bilgisi = models.TextField(blank=True, null=True, verbose_name="Not")
    olusturma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturma Tarihi")

    class Meta:
        verbose_name = "Sipariş"
        verbose_name_plural = "Siparişler"
        ordering = ["-siparis_tarihi"]

    def __str__(self):
        return f"{self.siparis_no} - {self.musteri.ad} - {self.siparis_tarihi}"

    def get_toplam_tutar(self):
        return self.miktar * self.fiyat
