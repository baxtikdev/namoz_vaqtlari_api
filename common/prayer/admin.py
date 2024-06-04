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
    exclude = ['created_at', 'updated_at']
