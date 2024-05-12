from django.contrib import admin

from common.prayer.models import PrayerTime, TakbirTime, IntervalTime


@admin.register(PrayerTime)
class PrayerTimeAdmin(admin.ModelAdmin):
    pass


@admin.register(TakbirTime)
class TakbirTimeAdmin(admin.ModelAdmin):
    pass


@admin.register(IntervalTime)
class IntervalTimeAdmin(admin.ModelAdmin):
    pass
