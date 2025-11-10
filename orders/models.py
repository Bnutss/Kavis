from django.db import models
from directory.models import Musteri
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os


class Urun(models.Model):
    """Ürün modeli - Товар"""
    ad = models.CharField(max_length=200, verbose_name="Ürün Adı")
    fiyat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Fiyat")
    fotograf = models.ImageField(upload_to='urunler/', verbose_name="Fotoğraf")
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    guncellenme_tarihi = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"
        ordering = ['-olusturulma_tarihi']

    def __str__(self):
        return self.ad

    def save(self, *args, **kwargs):
        if self.fotograf:
            img = Image.open(self.fotograf)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')

            output = BytesIO()
            img.save(output, format='WEBP', quality=85)
            output.seek(0)
            filename = os.path.splitext(self.fotograf.name)[0] + '.webp'
            self.fotograf.save(filename, ContentFile(output.read()), save=False)

        super().save(*args, **kwargs)


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
    musteri = models.ForeignKey(Musteri, on_delete=models.CASCADE, related_name='siparisler', verbose_name="Müşteri")

    # Выбор товара или ручной ввод
    urun = models.ForeignKey(Urun, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='siparisler', verbose_name="Ürün Seçimi")
    urun_cinsi = models.CharField(max_length=255, blank=True, verbose_name="Ürün Cinsi (Manuel)")

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

    def get_urun_adi(self):
        """Возвращает название товара из выбранного товара или ручного ввода"""
        if self.urun:
            return self.urun.ad
        return self.urun_cinsi or "Belirtilmemiş"

    def get_toplam_tutar(self):
        return self.miktar * self.fiyat

    def save(self, *args, **kwargs):
        # Автоматически заполнить цену из выбранного товара, если не указана
        if self.urun and not self.fiyat:
            self.fiyat = self.urun.fiyat
        super().save(*args, **kwargs)
