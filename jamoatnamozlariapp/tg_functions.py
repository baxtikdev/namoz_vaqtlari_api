from datetime import datetime
import logging
import os
from telebot import TeleBot
from telebot.types import InputFile
from UzTransliterator import UzTransliterator
# from .models import Masjid

bot = TeleBot(os.environ.get("BOT_TOKEN"), parse_mode="HTML")


text_uz = ""
text_cyrl = ""

months = {
    "uz": {
        1: "Yanvar",
        2: "Fevral",
        3: "Mart",
        4: "Aprel",
        5: "May",
        6: "Iyun",
        7: "Iyul",
        8: "Avgust",
        9: "Sentyabr",
        10: "Oktyabr",
        11: "Noyabr",
        12: "Dekabr",
    },
    "de": {
        1: "Январь",
        2: "Февраль",
        3: "Март",
        4: "Апрель",
        5: "Май",
        6: "Июнь",
        7: "Июль",
        8: "Август",
        9: "Сентябрь",
        10: "Октябрь",
        11: "Ноябрь",
        12: "Декабрь",
    },
}

def send_text(text):

    bot.send_message(chat_id=-1002111788540, text=text)

def send_backup(backup):
    try:
        bot.send_document(chat_id=-1002111788540, document=InputFile(backup), caption="#jamoatvaqtlari DB File | " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    except:
        bot.send_message(chat_id=1357813137, text="Error sending backup file | JamoatVaqtlariBot | " + datetime.now().strftime("%Y-%m-%d %H:%M"))

def get_photo_id(photo_file):

    ph = bot.send_photo(chat_id=-1002099528963, photo=photo_file)
    bot.reply_to(ph, "Rasm IDsi: " + ph.photo[-1].file_id)

    return ph.photo[-1].file_id

def send_new_masjid_times(masjid, subscriptions):
    obj = UzTransliterator.UzTransliterator()
    old, new = masjid
    current_time = datetime.now()
    azon = [new.bomdod, new.peshin, new.asr, new.shom, new.hufton]
    types = [new.bomdod_type, new.peshin_type, new.asr_type, new.shom_type, new.hufton_type]
    values = [new.bomdod_jamoat, new.peshin_jamoat, new.asr_jamoat, new.shom_jamoat, new.hufton_jamoat]
    times = [0, 0, 0, 0, 0]
        
    for i in range(0, 5):
        if types[i] == 'static':
            times[i] = values[i]
        else:
            if str(values[i]).isdigit():
                a, b = azon[i].split(":")
                a = int(a)
                b = int(b) + int(values[i])
                if b > 60:
                    a = int(a) + 1
                    b = b - 60
                times[i] = f"{'0' if int(a) < 10 else ''}{a}:{'0' if b < 10 else ''}{b}"
            else:
                times[i] = azon[i]
        
        new.bomdod_jamoat = times[0]
        new.peshin_jamoat = times[1]
        new.asr_jamoat = times[2]
        new.shom_jamoat = times[3]
        new.hufton_jamoat = times[4]

    text = f"""
 <b>{new.district.region.name_uz} {new.district.name_uz} {new.name_uz} namoz vaqtlari oʻzgardi.</b>

<i>🕒 Yangilangan vaqt: {current_time.day}|||{months['uz'][current_time.month].lower()}, {current_time.strftime("%H:%M")}</i>

<b>🏞 Bomdod:</b>
Azon – {new.bomdod} | Takbir – {new.bomdod_jamoat}

<b>🌇 Peshin:</b>
Azon – {new.peshin} | Takbir – {new.peshin_jamoat}

<b>🌆 Asr:</b>
Azon – {new.asr} | Takbir – {new.asr_jamoat}

<b>🌃 Shom:</b>
Azon – {new.shom} | Takbir – {new.shom_jamoat}

<b>🌌 Xufton:</b>
Azon – {new.hufton} | Takbir – {new.hufton_jamoat}"""

    for sub in subscriptions:
        
        try:
            if sub.user.lang == "de":
                bot.send_message(chat_id=sub.user.user_id, text=obj.transliterate(text, from_="lat", to="cyr").replace("|||", " ") + "\n\n@jamoatvaqtlaribot")
            elif sub.user.lang == "uz":
                bot.send_message(chat_id=sub.user.user_id, text=text.replace("|||", "-") + "\n\n@jamoatvaqtlaribot")
        except Exception as e:
            logging.warning(e)
    
def send_region_change_times(users, region, type):
    region_text = f"{region.district.region.name_uz} {region.district.name_uz}" if type == "district" else region.region.name_uz
    obj = UzTransliterator.UzTransliterator()
    current_time = datetime.now()
    text = f"""
 <b>🕌 {region_text} masjidlari namoz vaqtlari oʻzgardi.</b>

<i>🕒 Yangilangan vaqt: {current_time.day}|||{months['uz'][current_time.month].lower()}, {current_time.strftime("%H:%M")}</i>

<b>🏞 Bomdod:</b> {region.bomdod}

<b>🌇 Peshin:</b> {region.peshin}

<b>🌆 Asr:</b> {region.asr}

<b>🌃 Shom:</b> {region.shom}

<b>🌌 Xufton:</b> {region.xufton}"""
    
    for sub in users:
        try:
            if sub.user.lang == "de":
                bot.send_message(chat_id=sub.user.user_id, text=obj.transliterate(text, from_="lat", to="cyr").replace("|||", " ") + "\n\n@jamoatvaqtlaribot")
            elif sub.user.lang == "uz":
                bot.send_message(chat_id=sub.user.user_id, text=text.replace("|||", "-") + "\n\n@jamoatvaqtlaribot")

        except:
            pass