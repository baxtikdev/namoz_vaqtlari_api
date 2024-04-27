import datetime
from typing import List

from django.db.models import Count
from geopy.distance import geodesic
from ninja import NinjaAPI, Schema
from ninja.pagination import PageNumberPagination, paginate
from rest_framework import pagination
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from jamoatnamozlariapp.models import (
    District,
    Masjid,
    Mintaqa,
    User,
    Region,
    Subscription,
    TakbirVaqtlari,
    ChangeDistrictTimeSchedule
)
from jamoatnamozlariapp.serializer import NamozVaqtiSerializer, MasjidShortListSerializer

api = NinjaAPI()


class RegionSchema(Schema):
    pk: int
    name_uz: str
    name_ru: str
    name_cyrl: str


class DistrictSchema(Schema):
    pk: int
    name_uz: str
    name_ru: str
    name_cyrl: str
    region: RegionSchema


class TakbirSchema(Schema):
    bomdod: str | None
    peshin: str | None
    asr: str | None
    shom: str | None
    hufton: str | None


class MasjidlarListSchema(Schema):
    pk: int
    name_uz: str
    name_ru: str
    name_cyrl: str


class MasjidInfo(Schema):
    pk: int
    name_uz: str
    name_ru: str
    name_cyrl: str
    district: DistrictSchema
    photo: str | None
    photo_file: str | None
    bomdod: str
    peshin: str
    asr: str
    shom: str
    hufton: str
    bomdod_jamoat: str
    peshin_jamoat: str
    asr_jamoat: str
    shom_jamoat: str
    hufton_jamoat: str
    location: str | None
    last_update: datetime.datetime
    is_subscribed: bool = False


class UserSchema(Schema):
    pk: int
    full_name: str
    user_id: int


# class SubscriptionsSchema(Schema):
#     pk: int
#     masjid: MasjidInfo


class MintaqaSchema(Schema):
    pk: int
    name_uz: str
    name_ru: str
    name_cyrl: str
    mintaqa_id: str
    viloyat: str


class NamozVaqtiSchema(Schema):
    pk: int
    mintaqa: MintaqaSchema
    milodiy_oy: int
    milodiy_kun: int
    xijriy_oy: int
    xijriy_kun: int
    vaqtlari: str


class NamozVaqtiSchema2(Schema):
    pk: int
    district: DistrictSchema
    date: str
    bomdod: str
    peshin: str
    asr: str
    shom: str
    hufton: str


@api.post("/create-new-user")
def hello(request, name: str, chat_id, lang: str):
    try:
        User.objects.update_or_create(
            user_id=chat_id, defaults={"full_name": name, "lang": lang}
        )
        return {"success": "True"}
    except:
        return {"success": "False"}


@api.get("/get-regions", response=List[RegionSchema])
def get_regions(request):
    return Region.objects.filter(is_active=True)


@api.get("/get-districts", response=List[DistrictSchema])
def get_districts(request, pk):
    return District.objects.filter(region_id=pk, is_active=True)


@api.get("/get-masjidlar", response=List[MasjidlarListSchema])
@paginate(PageNumberPagination, page_size=5)
def get_masjidlar(request, district_id):
    return Masjid.objects.filter(district_id=district_id, is_active=True).order_by('id')


@api.get("/masjid-info")
def masjid_info(request, masjid_pk, user_id):
    masjid = Masjid.objects.select_related('district', 'district__region').filter(pk=masjid_pk).first()
    today = datetime.datetime.today().date()
    nomoz = ChangeDistrictTimeSchedule.objects.select_related('district').filter(
        district=masjid.district, date__date__lte=today).order_by('-date').first()
    takbir = TakbirVaqtlari.objects.filter(district=masjid.district, date__lte=today).order_by('-date')
    user = User.objects.get(user_id=user_id)
    is_subscribed = Subscription.objects.filter(masjid=masjid, user=user).exists()
    setattr(masjid, "is_subscribed", is_subscribed)

    takbir_data = {}
    if takbir:
        takbir_data["bomdod"] = takbir.first().bomdod
        takbir_data["peshin"] = takbir.first().peshin
        takbir_data["asr"] = takbir.first().asr
        takbir_data["shom"] = takbir.first().shom
        takbir_data["hufton"] = takbir.first().hufton
    data = {
        "pk": masjid.pk,
        "name_uz": masjid.name_uz,
        "name_ru": masjid.name_ru,
        "name_cyrl": masjid.name_cyrl,
        "district": {
            "pk": masjid.district.pk,
            "name_uz": masjid.district.name_uz,
            "name_ru": masjid.district.name_ru,
            "name_cyrl": masjid.district.name_cyrl,
            "region": {
                "pk": masjid.district.region.pk,
                "name_uz": masjid.district.region.name_uz,
                "name_ru": masjid.district.region.name_ru,
                "name_cyrl": masjid.district.region.name_cyrl
            }
        },
        "photo": masjid.photo,
        "photo_file": masjid.photo_file.url if masjid.photo_file else "",
        "date": nomoz.date if nomoz else "🕒",
        "bomdod": nomoz.bomdod if nomoz else "🕒",
        "peshin": nomoz.peshin if nomoz else "🕒",
        "asr": nomoz.asr if nomoz else "🕒",
        "shom": nomoz.shom if nomoz else "🕒",
        "hufton": nomoz.hufton if nomoz else "🕒",
        "bomdod_jamoat": masjid.bomdod_jamoat,
        "peshin_jamoat": masjid.peshin_jamoat,
        "asr_jamoat": masjid.asr_jamoat,
        "shom_jamoat": masjid.shom_jamoat,
        "hufton_jamoat": masjid.hufton_jamoat,
        "location": masjid.location,
        "last_update": masjid.last_update,
        "is_subscribed": masjid.is_subscribed,
        "takbir": takbir_data
    }
    return data


@api.get("/masjid-statistikasi")
def masjid_statistikasi(request, masjid_pk):
    masjid = Masjid.objects.get(pk=masjid_pk)
    statistic = masjid.get_leaderboard_position()

    return {
        "success": True,
        "name_uz": masjid.name_uz,
        "name_ru": masjid.name_ru,
        "name_cyrl": masjid.name_cyrl,
        "district": {
            "pk": masjid.district.pk,
            "name_uz": masjid.district.name_uz,
            "name_ru": masjid.district.name_ru,
            "name_cyrl": masjid.district.name_cyrl,
            "region": {
                "pk": masjid.district.region.pk,
                "name_uz": masjid.district.region.name_uz,
                "name_ru": masjid.district.region.name_ru,
                "name_cyrl": masjid.district.region.name_cyrl,
            },
        },
        "statistic": statistic,
        "subscription_count": Subscription.objects.filter(masjid=masjid).count(),
    }


@api.post("/masjid-subscription")
def masjid_subscription(request, user_id, masjid_id, action):
    if action == "subscribe_to":
        try:
            user = User.objects.get(user_id=user_id)
            masjid = Masjid.objects.get(pk=masjid_id)
            Subscription.objects.get_or_create(
                user=user,
                masjid=masjid,
            )
            return {
                "success": "True",
                "masjid": {
                    "pk": masjid.pk,
                    "name_uz": masjid.name_uz,
                    "name_ru": masjid.name_ru,
                    "name_cyrl": masjid.name_cyrl,
                    "district": {
                        "pk": masjid.district.pk,
                        "name_uz": masjid.district.name_uz,
                        "name_ru": masjid.district.name_ru,
                        "name_cyrl": masjid.district.name_cyrl,
                    },
                },
            }
        except:
            return {"success": "False"}
    elif action == "unsubscribe":
        try:
            user = User.objects.get(user_id=user_id)
            masjid = Masjid.objects.get(pk=masjid_id)
            Subscription.objects.filter(
                user=user,
                masjid=masjid,
            ).delete()
            return {
                "success": "True",
                "masjid": {
                    "pk": masjid.pk,
                    "name_uz": masjid.name_uz,
                    "name_ru": masjid.name_ru,
                    "name_cyrl": masjid.name_cyrl,
                    "district": {
                        "pk": masjid.district.pk,
                        "name_uz": masjid.district.name_uz,
                        "name_ru": masjid.district.name_ru,
                        "name_cyrl": masjid.district.name_cyrl,
                    },
                },
            }
        except:
            return {"success": "False"}
    return {"success": "False"}


@api.get("/user-subscriptions", response=List[MasjidInfo])
@paginate(PageNumberPagination, page_size=5)
def user_subscriptions(request, user_id):
    masjids = Masjid.objects.filter(masjidSubscription__user__user_id=user_id).distinct()
    return masjids


@api.get("/user-subscriptions-statistic")
def user_subscriptions(request, user_id):
    masjids = Subscription.objects.select_related('user', 'masjid', 'masjid__district',
                                                  'masjid__district__region').filter(user__user_id=user_id). \
        annotate(subscription_count=Count('masjid__masjidSubscription'))
    results = []
    for masjid in masjids:
        result = {
            "masjid": {
                "pk": masjid.masjid.pk,
                "name_uz": masjid.masjid.name_uz,
                "name_ru": masjid.masjid.name_ru,
                "name_cyrl": masjid.masjid.name_cyrl,
                "district": {
                    "pk": masjid.masjid.district.pk,
                    "name_uz": masjid.masjid.district.name_uz,
                    "name_ru": masjid.masjid.district.name_ru,
                    "name_cyrl": masjid.masjid.district.name_cyrl,
                    "region": {
                        "pk": masjid.masjid.district.region.pk,
                        "name_uz": masjid.masjid.district.region.name_uz,
                        "name_ru": masjid.masjid.district.region.name_ru,
                        "name_cyrl": masjid.masjid.district.region.name_cyrl,
                    },
                },
                "statistic": masjid.masjid.get_leaderboard_position(),
                "subscription_count": masjid.subscription_count,
            },
        }
        results.append(result)
    return results


# @api.get("/bugungi-namoz-vaqti", response=NamozVaqtiSchema2)
# def bugungi_namoz_vaqti(request, mintaqa, milodiy_oy, milodiy_kun):
#     currint_time = datetime.datetime.now()
#     t = ChangeDistrictTimeSchedule.objects.filter(
#         district_id=mintaqa,
#         date=currint_time.date()
#     )
#
#     print(t)
#     return t.last()
# return NamozVaqti.objects.filter(
#     mintaqa__mintaqa_id=mintaqa,
#     milodiy_oy=milodiy_oy,
#     milodiy_kun=milodiy_kun,
# ).first()


class BugungiNamozVaqtiAPIView(APIView):

    def get(self, request, *args, **kwargs):
        mintaqa = request.query_params.get("mintaqa")
        print(mintaqa)
        currint_time = datetime.datetime.now()
        t = ChangeDistrictTimeSchedule.objects.select_related('district').filter(
            district_id=mintaqa,
            date__date=currint_time.date()
        ).order_by('-date').first()
        if not t:
            return Response({}, status=status.HTTP_200_OK)

        data = NamozVaqtiSerializer(t).data
        return Response(data, status=status.HTTP_200_OK)


class NamozVaqtiAPIView(ListAPIView):
    queryset = ChangeDistrictTimeSchedule.objects.all().order_by('date')
    serializer_class = NamozVaqtiSerializer
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        mintaqa = self.request.query_params.get("mintaqa")
        currint_time = datetime.datetime.now()
        queryset = queryset.select_related('district').filter(date__month=currint_time.date().month)
        if mintaqa:
            queryset = queryset.filter(district_id=mintaqa)
        # for i in range(1, 31):
        #     start = datetime.datetime(2024, 6, i, 12, 30, 0)
        #     bomdod = '03:20'
        #     peshin = '13:00'
        #     asr = '17:10'
        #     shom = '19:18'
        #     hufton = '20:45'
        #     ChangeDistrictTimeSchedule.objects.get_or_create(district_id=11, date=start, bomdod=bomdod, peshin=peshin,
        #                                                      asr=asr, shom=shom, hufton=hufton)
        return queryset


class ClosestMasjidAPIView(APIView):
    def get(self, request, *args, **kwargs):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')
        masjids = Masjid.objects.filter(is_active=True, location__isnull=False).order_by('id')
        masjid_distances = []
        for masjid in masjids:
            try:
                masjid_latitude = masjid.location.split('@')[1].split(',')[0]
                masjid_longitude = masjid.location.split('@')[1].split(',')[1]
            except:
                # print("ERROR", masjid.name_uz)
                continue
            masjid_coordinates = (masjid_latitude, masjid_longitude)
            distance = geodesic((latitude, longitude), masjid_coordinates).kilometers
            masjid_distances.append((masjid, distance))
        closest_masjids = sorted(masjid_distances, key=lambda x: x[1])
        closest_masjids = list(map(lambda x: x[0], closest_masjids))[:5]
        return Response(MasjidShortListSerializer(closest_masjids, many=True).data)


# @api.get("/namoz-vaqtlari", response=List[NamozVaqtiSchema2])
# @paginate(PageNumberPagination, page_size=5)
# def namoz_vaqtlari(request, mintaqa, oy):
#     currint_time = datetime.datetime.now()
#     return ChangeDistrictTimeSchedule.objects.select_related('district').filter(
#         district_id=mintaqa,
#         date__month=currint_time.date().month
#     ).order_by('date')


@api.get("/viloyat-mintaqalari", response=List[MintaqaSchema])
def viloyat_mintaqalari(request, viloyat_id):
    return Mintaqa.objects.filter(viloyat=viloyat_id)


@api.get("mintaqa-malumotlari", response=MintaqaSchema)
def mintaqa_malumotlari(request, mintaqa_id):
    return Mintaqa.objects.get(mintaqa_id=mintaqa_id)
