from django.contrib import admin
from .models import Musteri


@admin.register(Musteri)
class MusteriAdmin(admin.ModelAdmin):
    list_display = ("ad", "ulke", "eposta", "aktif")
    list_filter = ("ulke", "aktif")
    search_fields = ("ad", "eposta")
    list_editable = ("aktif",)
