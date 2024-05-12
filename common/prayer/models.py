from datetime import time

from django.db import models
from django.utils import timezone

from common.base import BaseModel
from jamoatnamozlariapp.models import District


class PrayerTime(BaseModel):
    bomdod = models.TimeField(verbose_name="Bomdod", default=time(hour=0, minute=0))
    quyosh = models.TimeField(verbose_name="Quyosh", default=time(hour=0, minute=0))
    peshin = models.TimeField(verbose_name="Peshin", default=time(hour=0, minute=0))
    asr = models.TimeField(verbose_name="Asr", default=time(hour=0, minute=0))
    shom = models.TimeField(verbose_name="Shom", default=time(hour=0, minute=0))
    hufton = models.TimeField(verbose_name="Xufton", default=time(hour=0, minute=0))
    date = models.DateField(verbose_name="Sana")

    def __str__(self):
        return f"{self.date} - {self.bomdod} | {self.peshin} | {self.asr} | {self.shom} | {self.hufton}"

    class Meta:
        verbose_name = "Namoz vaqti"
        verbose_name_plural = "Namoz vaqtlari"


class TakbirTime(BaseModel):
    bomdod = models.TimeField(verbose_name="Bomdod", default=time(hour=0, minute=0))
    quyosh = models.TimeField(verbose_name="Quyosh", default=time(hour=0, minute=0))
    peshin = models.TimeField(verbose_name="Peshin", default=time(hour=0, minute=0))
    asr = models.TimeField(verbose_name="Asr", default=time(hour=0, minute=0))
    shom = models.TimeField(verbose_name="Shom", default=time(hour=0, minute=0))
    hufton = models.TimeField(verbose_name="Xufton", default=time(hour=0, minute=0))
    date = models.DateField(verbose_name="Sana", default=timezone.now)

    def __str__(self):
        return f"{self.date} - {self.bomdod} | {self.peshin} | {self.asr} | {self.shom} | {self.hufton}"

    class Meta:
        verbose_name = "Takbir vaqti"
        verbose_name_plural = "Takbir vaqtlari"


class IntervalTime(BaseModel):
    district = models.ForeignKey(District, related_name='districtIntervalTime', on_delete=models.CASCADE,
                                 verbose_name="Tuman")
    bomdod = models.TimeField(verbose_name="Bomdod", default=time(hour=0, minute=0))
    quyosh = models.TimeField(verbose_name="Quyosh", default=time(hour=0, minute=0))
    peshin = models.TimeField(verbose_name="Peshin", default=time(hour=0, minute=0))
    asr = models.TimeField(verbose_name="Asr", default=time(hour=0, minute=0))
    shom = models.TimeField(verbose_name="Shom", default=time(hour=0, minute=0))
    hufton = models.TimeField(verbose_name="Xufton", default=time(hour=0, minute=0))
    date = models.DateField(verbose_name="Sana", default=timezone.now)

    def __str__(self):
        return f"{self.date} - {self.bomdod} | {self.peshin} | {self.asr} | {self.shom} | {self.hufton}"

    class Meta:
        verbose_name = "Viloyat namoz vaqti farqi"
        verbose_name_plural = "Viloyat namoz vaqti farqlari"
