from django.contrib import admin
from .models import Siparis


@admin.register(Siparis)
class SiparisAdmin(admin.ModelAdmin):
    list_display = (
        "siparis_no",
        "musteri",
        "urun_cinsi",
        "miktar",
        "fiyat",
        "siparis_tarihi",
        "sevk_tarihi",
        "durum",
        "olusturma_tarihi",
    )
    list_filter = ("durum", "siparis_tarihi", "sevk_tarihi", "uretici")
    search_fields = ("siparis_no", "musteri__ad", "uretici", "not_bilgisi")
    readonly_fields = ("olusturma_tarihi",)
    ordering = ("-siparis_tarihi",)
    fieldsets = (
        (None, {
            "fields": (
                "siparis_no",
                "musteri",
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
