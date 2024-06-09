from django.contrib import admin

from common.prayer.models import PrayerTime, TakbirTime, IntervalTime


@admin.register(PrayerTime)
class PrayerTimeAdmin(admin.ModelAdmin):
    exclude = ['created_at', 'updated_at']


@admin.register(TakbirTime)
class TakbirTimeAdmin(admin.ModelAdmin):
    exclude = ['created_at', 'updated_at']


@admin.register(IntervalTime)
class IntervalTimeAdmin(admin.ModelAdmin):
    list_display = ['district', 'date', 'bomdod', 'peshin', 'asr', 'shom', 'hufton']
    exclude = ['created_at', 'updated_at']

    def district(self, obj):
        return obj.district.title

    def bomdod(self, obj):
        return obj.bomdod

    def peshin(self, obj):
        return obj.peshin

    def asr(self, obj):
        return obj.asr

    def shom(self, obj):
        return obj.shom

    def hufton(self, obj):
        return obj.hufton
