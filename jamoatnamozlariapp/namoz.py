# import datetime
#
# from rest_framework.viewsets import ModelViewSet
#
# from jamoatnamozlariapp.models import Masjid, ChangeDistrictTimeSchedule, TakbirVaqtlari, User, Subscription
#
#
# class PermissionAPIView(ModelViewSet):
#     queryset = Permission.objects.prefetch_related('content_type').all()
#     serializer_class = PermissionSerializer
#
#     def list(self, request, *args, **kwargs):
#         masjid = Masjid.objects.select_related('district', 'district__region').filter(pk=masjid_pk).first()
#         today = datetime.datetime.today().date()
#         nomoz = ChangeDistrictTimeSchedule.objects.select_related('district').filter(
#             district=masjid.district, date__date__lte=today).order_by('-date').first()
#         takbir = TakbirVaqtlari.objects.filter(district=masjid.district, date__lte=today).order_by('-date')
#         user = User.objects.get(user_id=user_id)
#         is_subscribed = Subscription.objects.filter(masjid=masjid, user=user).exists()
#         setattr(masjid, "is_subscribed", is_subscribed)
#
#         takbir_data = {}
#         if takbir:
#             takbir_data["bomdod"] = takbir.first().bomdod
#             takbir_data["peshin"] = takbir.first().peshin
#             takbir_data["asr"] = takbir.first().asr
#             takbir_data["shom"] = takbir.first().shom
#             takbir_data["hufton"] = takbir.first().hufton
#         data = {
#             "pk": masjid.pk,
#             "name_uz": masjid.name_uz,
#             "name_ru": masjid.name_ru,
#             "name_cyrl": masjid.name_cyrl,
#             "district": {
#                 "pk": masjid.district.pk,
#                 "name_uz": masjid.district.name_uz,
#                 "name_ru": masjid.district.name_ru,
#                 "name_cyrl": masjid.district.name_cyrl,
#                 "region": {
#                     "pk": masjid.district.region.pk,
#                     "name_uz": masjid.district.region.name_uz,
#                     "name_ru": masjid.district.region.name_ru,
#                     "name_cyrl": masjid.district.region.name_cyrl
#                 }
#             },
#             "photo": masjid.photo,
#             "photo_file": masjid.photo_file.url if masjid.photo_file else "",
#             "date": nomoz.date if nomoz else "🕒",
#             "bomdod": nomoz.bomdod if nomoz else "🕒",
#             "peshin": nomoz.peshin if nomoz else "🕒",
#             "asr": nomoz.asr if nomoz else "🕒",
#             "shom": nomoz.shom if nomoz else "🕒",
#             "hufton": nomoz.hufton if nomoz else "🕒",
#             "bomdod_jamoat": masjid.bomdod_jamoat,
#             "peshin_jamoat": masjid.peshin_jamoat,
#             "asr_jamoat": masjid.asr_jamoat,
#             "shom_jamoat": masjid.shom_jamoat,
#             "hufton_jamoat": masjid.hufton_jamoat,
#             "location": masjid.location,
#             "last_update": masjid.last_update,
#             "is_subscribed": masjid.is_subscribed,
#             "takbir": takbir_data
#         }
#         return data