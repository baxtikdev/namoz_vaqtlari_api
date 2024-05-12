from django.db import models

from common.base import BaseModel
from jamoatnamozlariapp.models import District


# class Region(BaseModel):
#     name_uz = models.CharField(max_length=255, verbose_name="Lotin", help_text="Viloyatning lotincha nomi")
#     name_cyrl = models.CharField(max_length=255, verbose_name="Kirill", help_text="Viloyatning kirillcha nomi")
#     name_ru = models.CharField(max_length=255, verbose_name="Rus", help_text="Viloyatning ruscha nomi")
#     is_active = models.BooleanField(default=True, verbose_name="Faolmi?")
#
#     class Meta:
#         verbose_name = "Viloyat"
#         verbose_name_plural = "Viloyatlar"
#
#
# class District(BaseModel):
#     region = models.ForeignKey(Region, related_name="regionDistrict", on_delete=models.CASCADE)
#     name_uz = models.CharField(max_length=255, verbose_name="Lotin", help_text="Tumanning lotincha nomi")
#     name_cyrl = models.CharField(max_length=255, verbose_name="Kirill", help_text="Tumanning kirillcha nomi")
#     name_ru = models.CharField(max_length=255, verbose_name="Rus", help_text="Tumanning ruscha nomi")
#     is_active = models.BooleanField(default=True, verbose_name="Faolmi?")
#
#     def __str__(self):
#         return self.name_uz
#
#     class Meta:
#         verbose_name = "Tuman"
#         verbose_name_plural = "Tumanlar"


class Mosque(BaseModel):
    district = models.ForeignKey(District, related_name='districtMosque', on_delete=models.CASCADE,
                                 verbose_name="Tuman")
    name_uz = models.CharField(max_length=255, verbose_name="Lotin", help_text="Masjidning lotincha nomi")
    name_cyrl = models.CharField(max_length=255, verbose_name="Kirill", help_text="Masjidning krillcha nomi")
    name_ru = models.CharField(max_length=255, verbose_name="Rus", help_text="Masjidning ruscha nomi")
    photo = models.ImageField(upload_to='imageMosque', verbose_name="Rasm", help_text="Masjidning rasmi", null=True,
                              blank=True)
    location = models.CharField(max_length=500, verbose_name="Manzil", help_text="Masjid manzili", null=True,
                                blank=True)
    description = models.TextField(verbose_name="Qisqa tavsif", help_text="Masjid haqida qisqa tavsif", null=True,
                                   blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    def __str__(self):
        return self.name_uz

    class Meta:
        verbose_name = "Masjid"
        verbose_name_plural = "Masjidlar"
