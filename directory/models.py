from django.db import models


class Musteri(models.Model):
    ad = models.CharField(max_length=255, verbose_name="Müşteri Adı")
    ulke = models.CharField(max_length=100, verbose_name="Ülke")
    eposta = models.EmailField(verbose_name="E-posta")
    aktif = models.BooleanField(default=True, verbose_name="Aktif Mi")

    class Meta:
        verbose_name = "Müşteri"
        verbose_name_plural = "Müşteriler"
        ordering = ["ad"]

    def __str__(self):
        return self.ad
