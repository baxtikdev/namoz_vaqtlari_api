from rest_framework import serializers

from common.prayer.models import PrayerTime, IntervalTime
from jamoatnamozlariapp.models import Region, District, Masjid, User


class RegionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["id", 'name_uz', 'name_cyrl', 'name_ru']


class DistrictListSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ["id", 'name_uz', 'name_cyrl', 'name_ru']


class DistrictDetailSerializer(serializers.ModelSerializer):
    region = RegionListSerializer()

    class Meta:
        model = District
        fields = ["id", 'name_uz', 'name_cyrl', 'name_ru', 'region']


class MasjidListSerializer(serializers.ModelSerializer):
    followerCount = serializers.SerializerMethodField()
    isFollowed = serializers.SerializerMethodField()

    def get_followerCount(self, masjid):
        if hasattr(masjid, 'followerCount'):
            return masjid.followerCount
        return 0

    def get_isFollowed(self, masjid):
        if hasattr(masjid, 'isFollowed'):
            return masjid.isFollowed
        return False

    class Meta:
        model = Masjid
        fields = ["id", 'name_uz', 'name_cyrl', 'name_ru', 'followerCount', 'isFollowed']


class MasjidDetailSerializer(serializers.ModelSerializer):
    district = DistrictDetailSerializer()
    isFollowed = serializers.SerializerMethodField()

    def get_isFollowed(self, masjid):
        if hasattr(masjid, 'isFollowed'):
            return masjid.isFollowed
        return False

    class Meta:
        model = Masjid
        fields = ["id", 'name_uz', 'name_cyrl', 'name_ru', 'district', 'photo', 'location', 'description', 'isFollowed']


class UserCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(required=True, max_length=30)

    class Meta:
        model = User
        fields = ['id', 'user_id', 'full_name']


class IntervalTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntervalTime
        fields = ['id', 'bomdod', 'quyosh', 'peshin', 'asr', 'shom', 'hufton', 'date']


class PrayerTimeListSerializer(serializers.ModelSerializer):
    interval = serializers.SerializerMethodField()

    def get_interval(self, prayer_time):
        if self.context.get('interval'):
            interval = self.context.get('interval').filter(date=prayer_time.date).first()
            if interval is None:
                interval = self.context.get('interval').filter(date__lt=prayer_time.date).order_by('-date').first()
                if interval is None:
                    interval = self.context.get('interval').order_by('date').first()
            return IntervalTimeSerializer(interval).data
        return None

    class Meta:
        model = PrayerTime
        fields = ['id', 'bomdod', 'quyosh', 'peshin', 'asr', 'shom', 'hufton', 'date', 'interval']
