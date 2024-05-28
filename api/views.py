from datetime import datetime, timedelta, time

from django.db.models import Exists, OuterRef, Count
from django.utils import timezone
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response

from api.paginator import CustomPagination
from api.serializers import RegionListSerializer, DistrictListSerializer, MasjidListSerializer, MasjidDetailSerializer, \
    UserCreateSerializer, PrayerTimeListSerializer, DistrictDetailSerializer
from common.prayer.models import PrayerTime, IntervalTime
from jamoatnamozlariapp.models import Region, District, Masjid, Subscription, User


class RegionListAPIView(ListAPIView):
    queryset = Region.objects.filter(is_active=True).all()
    serializer_class = RegionListSerializer
    pagination_class = CustomPagination


class DistrictListAPIView(ListAPIView):
    queryset = District.objects.filter(is_active=True).all()
    serializer_class = DistrictListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        region = self.request.query_params.get('region')
        if region:
            queryset = queryset.filter(region_id=region)
        return queryset


class DistrictDetailAPIView(RetrieveAPIView):
    queryset = District.objects.filter(is_active=True).all()
    serializer_class = DistrictDetailSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = super().get_queryset()
        region = self.request.query_params.get('region')
        if region:
            queryset = queryset.filter(region_id=region)
        return queryset


class MasjidListAPIView(ListAPIView):
    queryset = Masjid.objects.select_related('district', 'district__region').filter(is_active=True).all()
    serializer_class = MasjidListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        district = self.request.query_params.get('district')
        if district:
            queryset = queryset.filter(district_id=district)

        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.annotate(isFollowed=Exists(Subscription.objects.select_related('user'). \
                                                           filter(user__user_id=user_id, masjid_id=OuterRef('pk'))))
            queryset = queryset.filter(isFollowed=True).annotate(
                followerCount=Count('masjidSubscription', distinct=True))
        return queryset


class MasjidDetailAPIView(RetrieveAPIView):
    queryset = Masjid.objects.select_related('district', 'district__region').all()
    serializer_class = MasjidDetailSerializer
    pagination_class = CustomPagination
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        isFollow = self.request.query_params.get('isFollow')
        if user_id:
            user = User.objects.filter(user_id=user_id).first()
            follower = Subscription.objects.filter(masjid_id=self.kwargs.get('pk'),
                                                   user=user).first()
            if isFollow == '1' and follower is None:
                follower = Subscription.objects.get_or_create(masjid_id=self.kwargs.get('pk'),
                                                              user=user)
            if isFollow == '0':
                follower.delete()
            queryset = queryset.annotate(isFollowed=Exists(Subscription.objects.select_related('user'). \
                                                           filter(user=user, masjid_id=OuterRef('pk'))))
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        prayerTime = PrayerTime.objects.filter(date=timezone.now().date()).first()
        interval = IntervalTime.objects.filter(district=instance.district)

        serializer = self.get_serializer(instance)
        return Response(data={
            **serializer.data,
            'prayerTime': PrayerTimeListSerializer(prayerTime, context={'interval': interval}).data,
        })


class UserAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        user = User.objects.filter(user_id=request.data.get('user_id')).first()
        if user is None:
            User.objects.create(user_id=request.data.get('user_id'), full_name=request.data.get('full_name'))
        if user.full_name != request.data.get('full_name'):
            user.full_name = request.data.get('full_name')
            user.save()
        return Response(status=200)


class PrayerTimeListAPIView(ListAPIView):
    queryset = PrayerTime.objects.all().order_by('date')
    serializer_class = PrayerTimeListSerializer

    # pagination_class = PageNumberPagination
    def get_serializer_context(self):
        context = super().get_serializer_context()
        district = self.request.query_params.get('district')
        if district:
            interval = IntervalTime.objects.filter(district_id=district)
            context['interval'] = interval
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(date__month=datetime.now().month)
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(date=date)
        # self.generate_prayer_times_for_months(4, 8)
        return queryset

    def generate_prayer_times_for_date(self, date):
        prayer_times = {
            'bomdod': time(hour=4, minute=30),
            'quyosh': time(hour=6, minute=0),
            'peshin': time(hour=12, minute=0),
            'asr': time(hour=15, minute=30),
            'shom': time(hour=18, minute=0),
            'hufton': time(hour=21, minute=0)
        }

        PrayerTime.objects.get_or_create(
            bomdod=prayer_times['bomdod'],
            quyosh=prayer_times['quyosh'],
            peshin=prayer_times['peshin'],
            asr=prayer_times['asr'],
            shom=prayer_times['shom'],
            hufton=prayer_times['hufton'],
            date=date
        )

    def generate_prayer_times_for_months(self, start_month, end_month):
        start_date = datetime(year=2024, month=start_month, day=1)
        end_date = datetime(year=2024, month=end_month, day=31)
        current_date = start_date
        while current_date <= end_date:
            self.generate_prayer_times_for_date(current_date)
            current_date += timedelta(days=1)
