import asyncio
from datetime import datetime

import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone
from bs4 import BeautifulSoup
from .models import Mintaqa, NamozVaqti
from UzTransliterator import UzTransliterator
from jamoatnamozlariapp.models import ChangeDistrictTimeSchedule, TakbirVaqtlari, Subscription
from namozvaqtlari.settings import env

logger = get_task_logger(__name__)

loop = asyncio.get_event_loop()

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


@shared_task(name='send_message_task', soft_time_limit=14400)
def send_message_task(user_id, message):
    BOT_TOKEN = env("BOT_TOKEN")
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': user_id, 'text': message, 'parse_mode': 'HTML'}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Error: {e}")
    return {"message": "Message has sent successfully"}


@shared_task(name='namoz_vaqtlarini yangilash', soft_time_limit=14400, queue='my_sequential_queue')
def update():
    try:
        print('Boshlandi')
        page = requests.get("https://islom.uz/")
        soup = BeautifulSoup(page.text, "html.parser")
        a = soup.find("select", {"name": "region"}).find_all("option")
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
            Mintaqa.objects.get_or_create(viloyat=mintaqa[2], name_uz=latn, name_cyrl=mintaqa[0], mintaqa_id=mintaqa[1])
        mintaqalar = Mintaqa.objects.all()
        print("Mintaqa olindi")
        for mintaqa in mintaqalar:
            page = requests.get(
                f"https://islom.uz/vaqtlar/{mintaqa.mintaqa_id}/{timezone.now().month}"
            )
            soup = BeautifulSoup(page.text, "html.parser")
            vaqtlar = soup.find(
                "table", {"class": "table table-bordered prayer_table"}
            ).find_all("tr")
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
                n, _ = NamozVaqti.objects.get_or_create(
                    mintaqa=mintaqa,
                    milodiy_oy=timezone.now().month,
                    milodiy_kun=int(text[1]),
                    xijriy_oy=hijri_month,
                    xijriy_kun=int(text[0]),
                    vaqtlari=f"{text[3]} | {text[4]} | {text[5]} | {text[6]} | {text[7]} | {text[8]}",
                )

        print("Oylik namoz vaqtlari yangilandi!")
    except Exception as e:
        print("Error: {0}".format(e))
        print("Vaqtlarni yangilashda xatolik yuz berdi!")


@shared_task(name='daily_send_message_task', soft_time_limit=14400, queue='my_sequential_queue')
def daily_send_message_task():
    today = datetime.today().date()
    takbir = TakbirVaqtlari.objects.select_related('district', 'district__region'). \
        filter(date__lte=today).order_by('-date').first()
    if takbir:
        subscriptions = Subscription.objects.select_related('user').values_list('user__user_id',
                                                                                'user__lang').distinct()
        unique_user_lang_list = list(subscriptions)
        for subscription in unique_user_lang_list:
            azon = ChangeDistrictTimeSchedule.objects.select_related('district').filter(
                district=takbir.district, date__date__lte=today).order_by('-date').first()
            if subscription[1] == 'uz':
                sana = "Sana"
                tak = 'Takbir'
                az = 'Azon'
                # masjid = subscription.masjid.name_uz
                add = "dagi takbir vaqtlari o'zgardi"
                district = takbir.district.name_uz
                region = takbir.district.region.name_uz
            else:
                sana = "Сана"
                az = 'Азон'
                tak = 'Такбир'
                # masjid = subscription.masjid.name_cyrl
                add = "даги такбир вақтлари ўзгарди"
                district = takbir.district.name_cyrl
                region = takbir.district.region.name_cyrl
            # text = f"<b>🕌 {masjid}</b>\n\n"
            text = f"📍 <b>{region}, {district}{add}</b>\n\n"
            text += f"<b>📅 {sana}: {today.strftime('%d.%m.%Y')}</b>\n\n"
            if azon:
                text += f"<b>📣 {az}</b>: {azon.bomdod} | {azon.peshin} | {azon.asr} | {azon.shom} | {azon.hufton}\n\n"
            if takbir:
                text += f"<b>🕓 {tak}</b>: {takbir.bomdod} | {takbir.peshin} | {takbir.asr} | {takbir.shom} | {takbir.hufton}\n\n"
            send_message_task.apply_async(args=[subscription[0], text], queue='my_sequential_queue',
                                          time_limit=14400)
