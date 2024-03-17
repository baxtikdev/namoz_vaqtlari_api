import logging
from collections.abc import Iterable

from UzTransliterator import UzTransliterator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count
from django.utils import timezone

from .tg_functions import get_photo_id, send_new_masjid_times, send_region_change_times

viloyatlar = [
    ("1", "Toshkent shahri"),
    ("2", "Andijon"),
    ("3", "Buxoro"),
    ("4", "Fargʻona"),
    ("5", "Jizzax"),
    ("6", "Namangan"),
    ("7", "Navoiy"),
    ("8", "Qashqadaryo"),
    ("9", "Qoraqalpogʻiston"),
    ("10", "Samarqand"),
    ("11", "Sirdaryo"),
    ("12", "Surxondaryo"),
    ("13", "Toshkent viloyati"),
    ("14", "Xorazm"),
    ("99", "Boshqa"),
]


# Create your models here.
class User(models.Model):
    user_id = models.CharField(
        max_length=255,
        verbose_name="ID",
        help_text="Foydalanuvchining Telegramdagi ID'si",
    )
    full_name = models.TextField(
        null=True, blank=True, verbose_name="Ismi", help_text="Foydalanuvchi ismi"
    )
    lang = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Til", help_text="Til"
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"


class Admin(models.Model):
    user_id = models.CharField(
        max_length=255, verbose_name="ID", help_text="Adminning Telegramdagi ID'si"
    )
    full_name = models.CharField(
        max_length=255, verbose_name="Ismi", help_text="Admin ismi"
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Admin"
        verbose_name_plural = "Adminlar"


class Region(models.Model):
    name_uz = models.CharField(
        max_length=255,
        verbose_name="Lotin",
        help_text="Viloyatning lotincha nomi",
    )
    name_cyrl = models.CharField(
        max_length=255,
        verbose_name="Kirill",
        help_text="Viloyatning kirillcha nomi",
        null=True,
        blank=True,
    )
    name_ru = models.CharField(
        max_length=255,
        verbose_name="Rus",
        help_text="Viloyatning ruscha nomi",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Faolmi?",
        help_text="Faol bo'lmasa foydalanuvchilar ro'yxatida ko'rinmaydi",
    )

    def save(
            self,
            force_insert: bool = ...,
            force_update: bool = ...,
            using: str | None = ...,
            update_fields: Iterable[str] | None = ...,
    ) -> None:
        if self.name_cyrl == None:
            obj = UzTransliterator.UzTransliterator()
            self.name_cyrl = obj.transliterate(self.name_uz, from_="lat", to="cyr")
        if self.name_ru == None:
            self.name_ru = self.name_uz
        return super().save()

    def __str__(self):
        return self.name_uz

    class Meta:
        verbose_name = "Viloyat"
        verbose_name_plural = "Viloyatlar"


class District(models.Model):
    name_uz = models.CharField(
        max_length=255,
        verbose_name="Lotin",
        help_text="Tuman(shahar)ning lotincha nomi",
    )
    name_cyrl = models.CharField(
        max_length=255,
        verbose_name="Kirill",
        help_text="Tuman(shahar)ning kirillcha nomi",
        null=True,
        blank=True,
    )
    name_ru = models.CharField(
        max_length=255,
        verbose_name="Rus",
        help_text="Tuman(shahar)ning ruscha nomi",
        null=True,
        blank=True,
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        verbose_name="Viloyat",
        help_text="Tuman(shahar) joylashgan viloyat",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Faolmi?",
        help_text="Faol bo'lmasa foydalanuvchilar ro'yxatida ko'rinmaydi",
    )

    def save(
            self,
            force_insert: bool = ...,
            force_update: bool = ...,
            using: str | None = ...,
            update_fields: Iterable[str] | None = ...,
    ) -> None:
        if self.name_cyrl == None:
            obj = UzTransliterator.UzTransliterator()
            self.name_cyrl = obj.transliterate(self.name_uz, from_="lat", to="cyr")
        if self.name_ru == None:
            self.name_ru = self.name_uz
        return super().save()

    def __str__(self):
        return self.name_uz

    class Meta:
        verbose_name = "Tuman(shahar)"
        verbose_name_plural = "Tuman(shahar)lar"


class Masjid(models.Model):
    time_types = (("dynamic", "Dinamik"), ("static", "Statik"))
    name_uz = models.CharField(
        max_length=255, verbose_name="Lotin", help_text="Masjidning lotincha nomi"
    )
    name_cyrl = models.CharField(
        max_length=255,
        verbose_name="Kirill",
        help_text="Masjidning kirillcha nomi",
        null=True,
        blank=True,
    )
    name_ru = models.CharField(
        max_length=255,
        verbose_name="Rus",
        help_text="Masjidning ruscha nomi",
        null=True,
        blank=True,
    )
    photo = models.CharField(
        max_length=255,
        verbose_name="Rasm IDsi",
        help_text="Masjidning rasmi IDsi",
        null=True,
        blank=True,
    )
    photo_file = models.FileField(
        max_length=255,
        verbose_name="Rasm fayli",
        help_text="Masjidning rasm faylini yuklang",
        null=True,
        blank=True,
    )
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        verbose_name="Tuman(shahar)",
        help_text="Masjid joylashgan tuman(shahar)",
    )
    bomdod = models.CharField(
        max_length=255,
        verbose_name="Bomdod",
        help_text="Masjidda bomdod namozi oʻqilish vaqti",
        default="00:00",
        null=True,
        blank=True,
    )
    peshin = models.CharField(
        max_length=255,
        verbose_name="Peshin",
        help_text="Masjidda peshin namozi oʻqilish vaqti",
        default="00:00",
        null=True,
        blank=True,
    )
    asr = models.CharField(
        max_length=255,
        verbose_name="Asr",
        help_text="Masjidda asr namozi oʻqilish vaqti",
        default="00:00",
        null=True,
        blank=True,
    )
    shom = models.CharField(
        max_length=255,
        verbose_name="Shom",
        help_text="Masjidda shom namozi oʻqilish vaqti",
        default="00:00",
        null=True,
        blank=True,
    )
    hufton = models.CharField(
        max_length=255,
        verbose_name="Xufton",
        help_text="Masjidda xufton namozi oʻqilish vaqti",
        default="00:00",
        null=True,
        blank=True,
    )
    location = models.CharField(
        max_length=255,
        verbose_name="Manzil",
        help_text="Masjid manzili",
        null=True,
        blank=True,
    )
    qisqa_tavsif = models.TextField(
        verbose_name="Qisqa tavsif",
        help_text="Masjid haqida qisqa tavsif",
        null=True,
        blank=True,
    )

    bomdod_type = models.CharField(
        "Bomdod vaqti turi", max_length=255, choices=time_types, default="dynamic"
    )
    bomdod_jamoat = models.CharField(
        max_length=255,
        verbose_name="Bomdod jamoati",
        help_text="Masjidda bomdod namozi oʻqilish vaqti",
        default="0",
    )

    peshin_type = models.CharField(
        "Peshin vaqti turi", max_length=255, choices=time_types, default="dynamic"
    )
    peshin_jamoat = models.CharField(
        max_length=255,
        verbose_name="Peshin jamoati",
        help_text="Masjidda peshin namozi oʻqilish vaqti",
        default="0",
    )

    asr_type = models.CharField(
        "Asr vaqti turi", max_length=255, choices=time_types, default="dynamic"
    )
    asr_jamoat = models.CharField(
        max_length=255,
        verbose_name="Asr jamoati",
        help_text="Masjidda asr namozi oʻqilish vaqti",
        default="0",
    )

    shom_type = models.CharField(
        "Shom vaqti turi", max_length=255, choices=time_types, default="dynamic"
    )
    shom_jamoat = models.CharField(
        max_length=255,
        verbose_name="Shom jamoati",
        help_text="Masjidda shom namozi oʻqilish vaqti",
        default="0",
    )

    hufton_type = models.CharField(
        "Xufton vaqti turi", max_length=255, choices=time_types, default="dynamic"
    )
    hufton_jamoat = models.CharField(
        max_length=255,
        verbose_name="Xufton jamoati",
        help_text="Masjidda xufton namozi oʻqilish vaqti",
        default="0",
    )

    last_update = models.DateTimeField(auto_now=False, verbose_name="Yangilangan vaqti")
    is_active = models.BooleanField(
        default=True,
        verbose_name="Faolmi?",
        help_text="Faol bo'lmasa foydalanuvchilar ro'yxatida ko'rinmaydi",
    )

    def get_leaderboard_position(self) -> dict:
        all_masjids = Masjid.objects.annotate(
            subscribers_count=Count("masjidSubscription")
        ).order_by("-subscribers_count")
        district_masjids = (
            Masjid.objects.filter(district=self.district)
            .annotate(subscribers_count=Count("masjidSubscription"))
            .order_by("-subscribers_count")
        )
        region_masjids = (
            Masjid.objects.filter(district__region=self.district.region)
            .annotate(subscribers_count=Count("masjidSubscription"))
            .order_by("-subscribers_count")
        )

        all_position = (
            list(all_masjids).index(self) + 1 if self in all_masjids else None
        )
        district_position = (
            list(district_masjids).index(self) + 1 if self in district_masjids else None
        )
        region_position = (
            list(region_masjids).index(self) + 1 if self in region_masjids else None
        )

        return {
            "all_position": all_position,
            "district_position": district_position,
            "region_position": region_position,
        }

    def save(
            self,
            force_insert: bool = ...,
            force_update: bool = ...,
            using: str | None = ...,
            update_fields: Iterable[str] | None = ...,
            is_global_change=False,
    ) -> None:
        if self.name_ru == None:
            self.name_ru = self.name_uz
        if self.name_cyrl == None:
            obj = UzTransliterator.UzTransliterator()
            self.name_cyrl = obj.transliterate(self.name_uz, from_="lat", to="cyr")

        if self.photo_file:
            if not self.photo:
                self.photo = get_photo_id(self.photo_file.file)
            else:
                old = Masjid.objects.get(pk=self.pk)
                if self.photo_file != old.photo_file:
                    self.photo = get_photo_id(self.photo_file.file)

        types = [
            self.bomdod_type,
            self.peshin_type,
            self.asr_type,
            self.shom_type,
            self.hufton_type,
        ]
        jamoat_times = [
            self.bomdod_jamoat,
            self.peshin_jamoat,
            self.asr_jamoat,
            self.shom_jamoat,
            self.hufton_jamoat,
        ]
        for i in range(len(types)):
            if types[i] == "dynamic":
                if jamoat_times[i].isdigit():
                    pass
                else:
                    jamoat_times[i] = "0"
            elif types[i] == "static":
                pass

        if self.pk and not is_global_change:
            logging.warning(f"there was masjid so this is update")
            old = Masjid.objects.get(pk=self.pk)
            is_times_changed = False
            if self.bomdod != old.bomdod:
                is_times_changed = True
            if self.peshin != old.peshin:
                is_times_changed = True
            if self.asr != old.asr:
                is_times_changed = True
            if self.shom != old.shom:
                is_times_changed = True
            if self.hufton != old.hufton:
                is_times_changed = True
            if is_times_changed:
                self.last_update = timezone.now()
                subscriptions = self.subscription_set.all()
                super().save()
                send_new_masjid_times([old, self], subscriptions)
        else:
            pass
            self.last_update = timezone.now()
            super().save()
            logging.warning(f"there was no masjid so this is create")

        return

    def __str__(self):
        return self.name_uz

    class Meta:
        verbose_name = "Masjid"
        verbose_name_plural = "Masjidlar"


class ChangeMasjidTimeSchedule(models.Model):
    masjid = models.ForeignKey(Masjid, on_delete=models.CASCADE, verbose_name="Masjid")
    date = models.DateTimeField(verbose_name="Sana")
    bomdod = models.CharField(
        max_length=255,
        verbose_name="Bomdod",
        help_text="Masjidda bomdod namozi oʻqilish vaqti",
        default="00:00",
        null=True,
        blank=True,
    )
    peshin = models.CharField(
        max_length=255,
        verbose_name="Peshin",
        help_text="Masjidda peshin namozi oʻqilish vaqti",
        default="00:00",
        null=True,
        blank=True,
    )
    asr = models.CharField(
        max_length=255,
        verbose_name="Asr",
        help_text="Masjidda asr namozi oʻqilish vaqti",
        default="00:00",
        null=True,
        blank=True,
    )
    shom = models.CharField(
        max_length=255,
        verbose_name="Shom",
        help_text="Masjidda shom namozi oʻqilish vaqti",
        default="00:00",
        null=True,
        blank=True,
    )
    hufton = models.CharField(
        max_length=255,
        verbose_name="Xufton",
        help_text="Masjidda xufton namozi oʻqilish vaqti",
        default="00:00",
        null=True,
        blank=True,
    )
    is_notify = models.BooleanField(
        default=False,
        verbose_name="Xabar yuborish",
        help_text="Obunachilarga xabar yuborilsinmi?",
        choices=((True, "Ha"), (False, "Yo'q"))

    )

    def __str__(self):
        return f"{self.masjid.name_uz} jadvali"

    class Meta:
        verbose_name = "Masjid vaqtlarini oʻzgartirish jadvali"
        verbose_name_plural = "Masjid vaqtlarini oʻzgartirish jadvali"


class ChangeDistrictTimeSchedule(models.Model):
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, verbose_name="Tuman(Shahar)"
    )
    date = models.DateTimeField(verbose_name="Sana")
    bomdod = models.CharField(
        max_length=255,
        verbose_name="Bomdod",
        help_text="Masjidda bomdod namozi oʻqilish vaqti",
        default="00:00",
        null=True,
        blank=True,
    )
    peshin = models.CharField(
        max_length=255,
        verbose_name="Peshin",
        help_text="Masjidda peshin namozi oʻqilish vaqti",
        default="00:00",
        null=True,
        blank=True,
    )
    asr = models.CharField(
        max_length=255,
        verbose_name="Asr",
        help_text="Masjidda asr namozi oʻqilish vaqti",
        default="00:00",
        null=True,
        blank=True,
    )
    shom = models.CharField(
        max_length=255,
        verbose_name="Shom",
        help_text="Masjidda shom namozi oʻqilish vaqti",
        default="00:00",
        null=True,
        blank=True,
    )
    hufton = models.CharField(
        max_length=255,
        verbose_name="Xufton",
        help_text="Masjidda xufton namozi oʻqilish vaqti",
        default="00:00",
        null=True,
        blank=True,
    )
    is_notify = models.BooleanField(
        default=False,
        verbose_name="Xabar yuborish",
        help_text="Obunachilarga xabar yuborilsinmi?",
        choices=((True, "Ha"), (False, "Yo'q"))
    )

    def __str__(self):
        return f"{self.district.name_uz}({self.date}) - {self.bomdod} | {self.peshin} | {self.asr} | {self.shom} | {self.hufton}"

    class Meta:
        verbose_name = "Tuman(Shahar) vaqtlarini oʻzgartirish jadvali"
        verbose_name_plural = "Tuman(Shahar) vaqtlarini oʻzgartirish jadvali"


class ChangeRegionTimeSchedule(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Viloyat")
    date = models.DateTimeField(verbose_name="Sana")
    bomdod = models.CharField(
        max_length=255,
        verbose_name="Bomdod",
        help_text="Masjidda bomdod namozi oʻqilish vaqti",
        default="00:00",
        null=True,
        blank=True,
    )
    peshin = models.CharField(
        max_length=255,
        verbose_name="Peshin",
        help_text="Masjidda peshin namozi oʻqilish vaqti",
        default="00:00",
        null=True,
        blank=True,
    )
    asr = models.CharField(
        max_length=255,
        verbose_name="Asr",
        help_text="Masjidda asr namozi oʻqilish vaqti",
        default="00:00",
        null=True,
        blank=True,
    )
    shom = models.CharField(
        max_length=255,
        verbose_name="Shom",
        help_text="Masjidda shom namozi oʻqilish vaqti",
        default="00:00",
        null=True,
        blank=True,
    )
    hufton = models.CharField(
        max_length=255,
        verbose_name="Xufton",
        help_text="Masjidda xufton namozi oʻqilish vaqti",
        default="00:00",
        null=True,
        blank=True,
    )
    is_notify = models.BooleanField(
        default=False,
        verbose_name="Xabar yuborish",
        help_text="Obunachilarga xabar yuborilsinmi?",
        choices=((True, "Ha"), (False, "Yo'q"))

    )

    def __str__(self):
        return f"{self.region.name_uz} jadvali"

    class Meta:
        verbose_name = "Viloyat vaqtlarini oʻzgartirish jadvali"
        verbose_name_plural = "Viloyat vaqtlarini oʻzgartirish jadvali"


class CustomUser(AbstractUser):
    admin_types = (
        ("region", "Viloyat/Shaxar adminstratori"),
        ("district", "Tuman adminstratori"),
        ("masjid", "Masjid adminstratori"),
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Viloyat/Shaxar",
        help_text="Adminstratorga biriktiriladigan viloyat/shaxar",
    )
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Tuman",
        help_text="Adminstratorga biriktiriladigan tuman",
    )
    masjid = models.ForeignKey(
        Masjid,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Masjid",
        help_text="Adminstratorga biriktiriladigan masjid",
    )
    admin_type = models.CharField(
        max_length=255,
        verbose_name="Adminstrator turi",
        null=True,
        choices=admin_types,
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Adminstrator"
        verbose_name_plural = "Adminstratorlar"


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="userSubscription",
        verbose_name="Foydalanuvchi",
        help_text="Foydalanuvchi",
    )
    masjid = models.ForeignKey(
        Masjid,
        related_name="masjidSubscription",
        on_delete=models.CASCADE,
        verbose_name="Masjid",
        help_text="Masjid",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.user.full_name

    class Meta:
        verbose_name = "Obuna"
        verbose_name_plural = "Obunalar"


class Mintaqa(models.Model):
    name_uz = models.CharField(
        max_length=255, verbose_name="Lotin", help_text="Mintaqaning lotincha nomi"
    )
    name_cyrl = models.CharField(
        max_length=255,
        verbose_name="Kirill",
        help_text="Mintaqaning kirillcha nomi",
        null=True,
        blank=True,
    )
    name_ru = models.CharField(
        max_length=255,
        verbose_name="Rus",
        help_text="Mintaqaning ruscha nomi",
        null=True,
        blank=True,
    )
    mintaqa_id = models.CharField(
        max_length=255, verbose_name="Mintaqa IDsi", help_text="Mintaqaning IDsi"
    )
    viloyat = models.CharField(
        max_length=255,
        choices=viloyatlar,
        verbose_name="Viloyat",
        help_text="Mintaqa joylashgan viloyat",
    )

    def __str__(self):
        return self.name_uz

    class Meta:
        verbose_name = "Mintaqa"
        verbose_name_plural = "Mintaqalar"

    def save(
            self,
            force_insert: bool = ...,
            force_update: bool = ...,
            using: str | None = ...,
            update_fields: Iterable[str] | None = ...,
    ) -> None:
        if self.name_ru == None:
            self.name_ru = self.name_uz

        return super().save()


class NamozVaqti(models.Model):
    mintaqa = models.ForeignKey(
        Mintaqa, on_delete=models.CASCADE, verbose_name="Mintaqa", help_text="Mintaqa"
    )
    milodiy_oy = models.IntegerField(verbose_name="Milodiy oy", help_text="Milodiy oy")
    xijriy_oy = models.IntegerField(verbose_name="Xijriy oy", help_text="Xijriy oy")
    milodiy_kun = models.IntegerField(
        verbose_name="Milodiy kun", help_text="Milodiy kun"
    )
    xijriy_kun = models.IntegerField(verbose_name="Xijriy kun", help_text="Xijriy kun")
    vaqtlari = models.CharField(
        max_length=255,
        verbose_name="Vaqtlari",
        help_text="Tong | Quyosh | Peshin | Asr | Shom | Xufton",
    )

    def __str__(self):
        return self.mintaqa.name_uz

    class Meta:
        verbose_name = "Namoz vaqti"
        verbose_name_plural = "Namoz vaqtlari"


class ChangeJamoatVaqtlari(models.Model):
    time_types = (("dynamic", "Dinamik"), ("static", "Statik"))
    change_all = models.BooleanField(
        default=False,
        verbose_name="Barcha masjidlar",
        help_text="Barcha masjidlar ma'lumotlarini o'zgartirish",
    )
    change_region = models.BooleanField(
        verbose_name="Viloyatni o'zgartirish",
        help_text="Tanlangan viloyat masjidlari ma'lumotlarini o'zgartirish",
        default=False,
    )
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, verbose_name="Viloyat", null=True, blank=True
    )
    change_district = models.BooleanField(
        verbose_name="Tumanni o'zgartirish",
        help_text="Tanlangan tuman masjidlari ma'lumotlarini o'zgartirish",
        default=False,
    )
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, verbose_name="Tuman", null=True, blank=True
    )
    change_masjid = models.BooleanField(
        verbose_name="Masjidni o'zgartirish",
        help_text="Tanlangan masjid ma'lumotlarini o'zgartirish",
        default=False,
    )
    masjid = models.ForeignKey(
        Masjid, on_delete=models.CASCADE, verbose_name="Masjid", null=True, blank=True
    )

    bomdod_type = models.CharField(
        "Bomdod vaqti turi", max_length=255, choices=time_types, default="dynamic"
    )
    bomdod_jamoat = models.CharField(
        max_length=255,
        verbose_name="Bomdod jamoati",
        help_text="Masjidda bomdod namozi oʻqilish vaqti",
        default="0",
    )

    peshin_type = models.CharField(
        "Peshin vaqti turi", max_length=255, choices=time_types, default="dynamic"
    )
    peshin_jamoat = models.CharField(
        max_length=255,
        verbose_name="Peshin jamoati",
        help_text="Masjidda peshin namozi oʻqilish vaqti",
        default="0",
    )

    asr_type = models.CharField(
        "Asr vaqti turi", max_length=255, choices=time_types, default="dynamic"
    )
    asr_jamoat = models.CharField(
        max_length=255,
        verbose_name="Asr jamoati",
        help_text="Masjidda asr namozi oʻqilish vaqti",
        default="0",
    )

    shom_type = models.CharField(
        "Shom vaqti turi", max_length=255, choices=time_types, default="dynamic"
    )
    shom_jamoat = models.CharField(
        max_length=255,
        verbose_name="Shom jamoati",
        help_text="Masjidda shom namozi oʻqilish vaqti",
        default="0",
    )

    hufton_type = models.CharField(
        "Xufton vaqti turi", max_length=255, choices=time_types, default="dynamic"
    )
    hufton_jamoat = models.CharField(
        max_length=255,
        verbose_name="Xufton jamoati",
        help_text="Masjidda xufton namozi oʻqilish vaqti",
        default="0",
    )

    class Meta:
        verbose_name = "Jamoat vaqtini tahrirlash"
        verbose_name_plural = "Jamoat vaqtlarini tahrirlash"

    def save(
            self,
            force_insert: bool = ...,
            force_update: bool = ...,
            using: str | None = ...,
            update_fields: Iterable[str] | None = ...,
    ) -> None:
        if self.change_all:
            Masjid.objects.all().update(
                bomdod_type=self.bomdod_type,
                bomdod_jamoat=self.bomdod_jamoat,
                peshin_type=self.peshin_type,
                peshin_jamoat=self.peshin_jamoat,
                asr_type=self.asr_type,
                asr_jamoat=self.asr_jamoat,
                shom_type=self.shom_type,
                shom_jamoat=self.shom_jamoat,
                hufton_type=self.hufton_type,
                hufton_jamoat=self.hufton_jamoat,
            )
        else:
            if self.change_masjid:
                if self.masjid:
                    self.masjid.bomdod_jamoat = self.bomdod_jamoat
                    self.masjid.peshin_jamoat = self.peshin_jamoat
                    self.masjid.asr_jamoat = self.asr_jamoat
                    self.masjid.shom_jamoat = self.shom_jamoat
                    self.masjid.hufton_jamoat = self.hufton_jamoat
                    self.masjid.bomdod_type = self.bomdod_type
                    self.masjid.peshin_type = self.peshin_type
                    self.masjid.asr_type = self.asr_type
                    self.masjid.shom_type = self.shom_type
                    self.masjid.hufton_type = self.hufton_type
                    self.masjid.save()
            if self.change_region:
                if self.region:
                    masjids = Masjid.objects.filter(district__region=self.region)
                    masjids.update(
                        bomdod_type=self.bomdod_type,
                        bomdod_jamoat=self.bomdod_jamoat,
                        peshin_type=self.peshin_type,
                        peshin_jamoat=self.peshin_jamoat,
                        asr_type=self.asr_type,
                        asr_jamoat=self.asr_jamoat,
                        shom_type=self.shom_type,
                        shom_jamoat=self.shom_jamoat,
                        hufton_type=self.hufton_type,
                        hufton_jamoat=self.hufton_jamoat,
                    )
            if self.change_district:
                if self.district:
                    masjids = Masjid.objects.filter(district=self.district)
                    masjids.update(
                        bomdod_type=self.bomdod_type,
                        bomdod_jamoat=self.bomdod_jamoat,
                        peshin_type=self.peshin_type,
                        peshin_jamoat=self.peshin_jamoat,
                        asr_type=self.asr_type,
                        asr_jamoat=self.asr_jamoat,
                        shom_type=self.shom_type,
                        shom_jamoat=self.shom_jamoat,
                        hufton_type=self.hufton_type,
                        hufton_jamoat=self.hufton_jamoat,
                    )


class TakbirVaqtlari(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="Tuman", null=True, blank=True)
    bomdod = models.CharField(max_length=255, verbose_name="Bomdod jamoati",
                              help_text="Masjidda bomdod namozi oʻqilish vaqti", null=True, blank=True)
    peshin = models.CharField(max_length=255, verbose_name="Peshin jamoati",
                              help_text="Masjidda peshin namozi oʻqilish vaqti", null=True, blank=True)
    asr = models.CharField(max_length=255, verbose_name="Asr jamoati", help_text="Masjidda asr namozi oʻqilish vaqti",
                           null=True, blank=True)
    shom = models.CharField(max_length=255, verbose_name="Shom jamoati",
                            help_text="Masjidda shom namozi oʻqilish vaqti", null=True, blank=True)
    hufton = models.CharField(max_length=255, verbose_name="Xufton jamoati",
                              help_text="Masjidda xufton namozi oʻqilish vaqti", null=True, blank=True)
    date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = "Jamoat vaqtini tahrirlash"
        verbose_name_plural = "Jamoat vaqtlarini tahrirlash"

    def __str__(self):
        return f"{self.district.name_uz}({self.date}) - {self.bomdod} | {self.peshin} | {self.asr} | {self.shom} | {self.hufton}"


class ShaxarViloyatTimesChange(models.Model):
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, verbose_name="Shaxar/Viloyat"
    )
    bomdod = models.CharField(
        max_length=255, verbose_name="Bomdod", help_text="Bomdod vaqti"
    )
    peshin = models.CharField(
        max_length=255, verbose_name="Peshin", help_text="Peshin vaqti"
    )
    asr = models.CharField(max_length=255, verbose_name="Asr", help_text="Asr vaqti")
    shom = models.CharField(max_length=255, verbose_name="Shom", help_text="Shom vaqti")
    xufton = models.CharField(
        max_length=255, verbose_name="Xufton", help_text="Xufton vaqti"
    )

    def save(
            self,
            force_insert: bool = ...,
            force_update: bool = ...,
            using: str | None = ...,
            update_fields: Iterable[str] | None = ...,
    ) -> None:
        region_masjids = Masjid.objects.filter(district__region=self.region)
        users = set()
        for masjid in region_masjids:
            masjid.bomdod = self.bomdod
            masjid.peshin = self.peshin
            masjid.asr = self.asr
            masjid.shom = self.shom
            masjid.hufton = self.xufton
            masjid.save(is_global_change=True)
            subs = masjid.subscription_set.all()
            for sub in subs:
                users.add(sub)

        send_region_change_times(users, self, "region")

        # return super().save()

    class Meta:
        verbose_name = "Viloyat vaqtlarini oʻzgartirish"
        verbose_name_plural = "Viloyat vaqtlarini oʻzgartirish"


class TumanTimesChange(models.Model):
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, verbose_name="Tuman"
    )
    bomdod = models.CharField(
        max_length=255, verbose_name="Bomdod", help_text="Bomdod vaqti"
    )
    peshin = models.CharField(
        max_length=255, verbose_name="Peshin", help_text="Peshin vaqti"
    )
    asr = models.CharField(max_length=255, verbose_name="Asr", help_text="Asr vaqti")
    shom = models.CharField(max_length=255, verbose_name="Shom", help_text="Shom vaqti")
    xufton = models.CharField(
        max_length=255, verbose_name="Xufton", help_text="Xufton vaqti"
    )

    def save(
            self,
            force_insert: bool = ...,
            force_update: bool = ...,
            using: str | None = ...,
            update_fields: Iterable[str] | None = ...,
    ) -> None:
        tuman_masjids = Masjid.objects.filter(district=self.district)
        users = set()
        for masjid in tuman_masjids:
            masjid.bomdod = self.bomdod
            masjid.peshin = self.peshin
            masjid.asr = self.asr
            masjid.shom = self.shom
            masjid.hufton = self.xufton
            masjid.save(is_global_change=True)
            subs = masjid.subscription_set.all()
            for sub in subs:
                users.add(sub)

        send_region_change_times(users, self, "district")

        # return super().save()

    class Meta:
        verbose_name = "Tuman (shahar) vaqtlarini oʻzgartirish"
        verbose_name_plural = "Tuman (shahar) vaqtlarini oʻzgartirish"
