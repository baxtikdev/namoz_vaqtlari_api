from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

from jamoatnamozlariapp.models import TakbirVaqtlari, Subscription, ChangeDistrictTimeSchedule
from jamoatnamozlariapp.tasks import send_message_task


@receiver(post_save, sender=TakbirVaqtlari)
def takbirVaqtlariSave(sender, instance, created, **kwargs):
    today = datetime.today().date()
    if instance.date == today:
        takbir = TakbirVaqtlari.objects.select_related('district', 'district__region').filter(id=instance.id).first()
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
