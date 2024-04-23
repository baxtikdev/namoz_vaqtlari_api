from rest_framework import serializers

from jamoatnamozlariapp.models import ChangeDistrictTimeSchedule, District, Region


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['pk', 'name_uz', 'name_cyrl', 'name_ru']


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['pk', 'name_uz', 'name_cyrl', 'name_ru', 'region']


class NamozVaqtiSerializer(serializers.ModelSerializer):
    district = DistrictSerializer()

    class Meta:
        model = ChangeDistrictTimeSchedule
        fields = ['pk', 'district', 'date', 'bomdod', 'peshin', 'asr', 'shom', 'hufton']
