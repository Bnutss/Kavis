from django.contrib import admin
from .models import Urun, Siparis


@admin.register(Urun)
class UrunAdmin(admin.ModelAdmin):
    list_display = ['ad', 'fiyat', 'olusturulma_tarihi']
    search_fields = ['ad']
    readonly_fields = ('olusturulma_tarihi', 'guncellenme_tarihi')


@admin.register(Siparis)
class SiparisAdmin(admin.ModelAdmin):
    list_display = (
        "siparis_no",
        "musteri",
        "get_urun_display",
        "miktar",
        "fiyat",
        "siparis_tarihi",
        "sevk_tarihi",
        "durum",
        "olusturma_tarihi",
    )
    list_filter = ("durum", "siparis_tarihi", "sevk_tarihi", "uretici")
    search_fields = ("siparis_no", "musteri__ad", "uretici", "not_bilgisi", "urun__ad", "urun_cinsi")
    readonly_fields = ("olusturma_tarihi",)
    ordering = ("-siparis_tarihi",)
    fieldsets = (
        (None, {
            "fields": (
                "siparis_no",
                "musteri",
                "urun",
                "urun_cinsi",
                "miktar",
                "fiyat",
                "siparis_tarihi",
                "uretici",
                "sevk_tarihi",
                "durum",
                "not_bilgisi",
            )
        }),
        ("Ek Bilgiler", {
            "fields": ("olusturma_tarihi",),
            "classes": ("collapse",)
        }),
    )

    def get_urun_display(self, obj):
        return obj.get_urun_adi()

    get_urun_display.short_description = 'Ürün'
