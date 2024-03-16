import os
import time
from .tg_functions import send_backup, send_text
from django.utils import timezone
import logging
from bs4 import BeautifulSoup
import kronos
import random
import requests
from .models import Mintaqa, NamozVaqti, ChangeRegionTimeSchedule, ChangeMasjidTimeSchedule, ChangeDistrictTimeSchedule, TumanTimesChange, ShaxarViloyatTimesChange, Masjid 
from UzTransliterator import UzTransliterator
hijri_months = {
    1: "Муҳаррам, Muharram",
    2: "Сафар, Safar",
    3: "Рабиъул аввал, Rabi’ul avval",
    4: "Рабиъул ахир, Rabi’ul axir",
    5: "Жумадул аввал, Jumadul avval",
    6: "Жумадул ахир, Jumadul axir",
    7: "Ражаб, Rajab",
    8: "Шаъбон, Sha’bon",
    9: "Рамазон, Ramazon",
    10: "Шаввол, Shavvol",
    11: "Зул қаъда, Zul qa’da",
    12: "Зул ҳижжа, Zul hijja",
}

regions = {
    1: [27],  # toshkent
    2: [1, 28, 29, 30, 31, 49, 69, 73],  # andijon
    3: [4, 45, 46, 47, 48],  # buxoro
    4: [13, 26, 37, 38, 39, 40],  # fargona
    5: [9, 50, 51, 52, 53, 55, 56],  # jizzax
    6: [15, 32, 33, 34, 35, 36],  # namangan
    7: [14, 17, 58, 59, 60, 61, 62, 63, 64],  # navoiy
    8: [25, 84, 85, 86, 87, 88, 93],  # qashqadaryo
    9: [16, 65, 66, 67, 68, 70, 71],  # qoraqalpogiston
    10: [10, 11, 18, 72],  # Samarqand
    11: [5],  # sirdaryo
    12: [6, 74, 75, 76, 77],  # surxondaryo
    13: [2, 43, 44],  # tashkent viloyat
    14: [21, 78, 79, 80, 81, 82],  # xorazm
    99: [3, 7, 8, 12, 19, 20, 22, 23, 41, 42, 57, 89, 90, 91, 92],  # boshqa
}


@kronos.register("0 0 1 * *")
def update():
    try:
        page = requests.get("https://islom.uz/")
        soup = BeautifulSoup(page.text, "html.parser")
        # print(soup.prettify())
        a = soup.find("select", {"name": "region"}).findAll("option")
        mintaqalist = []
        for i in a:
            mtext = i.text
            mid = int(i["value"])
            mregion = 99
            for key, value in regions.items():
                if mid in value:
                    mregion = key

            mintaqalist.append([mtext, mid, mregion])

        obj = UzTransliterator.UzTransliterator()
        for mintaqa in mintaqalist:
            latn = obj.transliterate(mintaqa[0], from_="cyr", to="lat")
            a, b = Mintaqa.objects.get_or_create(
                viloyat=mintaqa[2], name_uz=latn, name_cyrl=mintaqa[0], mintaqa_id=mintaqa[1]
            )
            a.save()
        mintaqalar = Mintaqa.objects.all()
        for mintaqa in mintaqalar:
            page = requests.get(
                f"https://islom.uz/vaqtlar/{mintaqa.mintaqa_id}/{timezone.now().month}"
            )
            soup = BeautifulSoup(page.text, "html.parser")
            # print(soup.prettify())
            vaqtlar = soup.find(
                "table", {"class": "table table-bordered prayer_table"}
            ).findAll("tr")
            last_hijri = 0
            hijri_month = 0
            headers = vaqtlar.pop(0)
            for vaqt in vaqtlar:
                text = vaqt.text.split()
                if last_hijri > int(text[0]) or last_hijri == 0:
                    hijri_day = requests.get(
                        f"http://api.aladhan.com/v1/gToH/{text[1]}-{timezone.now().month}-{timezone.now().year}"
                    )
                    result = hijri_day.json()
                    hijri_month = result["data"]["hijri"]["month"]["number"]
                last_hijri = int(text[0])
                a, b = NamozVaqti.objects.get_or_create(
                    mintaqa=mintaqa,
                    milodiy_oy=timezone.now().month,
                    milodiy_kun=int(text[1]),
                    xijriy_oy=hijri_month,
                    xijriy_kun=int(text[0]),
                    vaqtlari=f"{text[3]} | {text[4]} | {text[5]} | {text[6]} | {text[7]} | {text[8]}",
                )
                a.save()

        send_text("Oylik namoz vaqtlari yangilandi!")
    except:
        send_text("Vaqtlarni yangilashda xatolik yuz berdi!")


@kronos.register("*/30 * * * *")
def backup():
    os.popen(f'7z a backup.zip /app/dbfile/db.sqlite3 -pJamoatVaqtlari@2024')
    time.sleep(10)
    send_backup("/root/backup.zip")

@kronos.register("*/10 * * * *")
def change_time():
    # Get the current time
    current_time = timezone.now()

    # Calculate the time threshold for 10 minutes
    time_threshold = timezone.timedelta(minutes=10)
    
    regions_to_change = ChangeRegionTimeSchedule.objects.exclude(date__gt=current_time + time_threshold)

    for region in regions_to_change:
        ShaxarViloyatTimesChange.objects.create(region=region.region, bomdod=region.bomdod, peshin=region.peshin, asr=region.asr, shom=region.shom, xufton=region.hufton)
        region.delete()
    
    districts_to_change = ChangeDistrictTimeSchedule.objects.exclude(date__gt=current_time + time_threshold)     

    for district in districts_to_change:
        TumanTimesChange.objects.create(district=district.district, bomdod=district.bomdod, peshin=district.peshin, asr=district.asr, shom=district.shom, xufton=district.hufton)
        district.delete()

    masjids_to_change = ChangeMasjidTimeSchedule.objects.exclude(date__gt=current_time + time_threshold)     

    for masjid in masjids_to_change:
        a = Masjid.objects.get(id=masjid.masjid_id)
        a.bomdod = masjid.bomdod
        a.peshin = masjid.peshin
        a.asr = masjid.asr
        a.shom = masjid.shom
        a.hufton = masjid.hufton
        a.save()
        masjid.delete()

    logging.warning("Time changed!")
    logging.warning(masjids_to_change)
    logging.warning(districts_to_change)
    logging.warning(regions_to_change)