# jamoatnamozlariapp/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    # path('newstat/', your_custom_view2, name='newstat'),
    path('masjid_s/', masjid_statistics, name='masjid_statistic'),
    path('region_s/', region_statistics, name='region_statistic'),
    path('district_s/', district_statistics, name='district_statistic'),
    path('region_list/', region_list_view, name='region_list'),
    path('region_detail/<int:pk>/', region_detail_view, name='region_detail'),
    path('masjids_in_district/<int:district_id>/', masjids_in_district_statistics, name='masjids_in_district_statistic'),
    path('masjids_in_region/<int:region_id>/', masjids_in_region_statistics, name='masjids_in_region_statistic'),
    path('districts_in_region/<int:region_id>/', districts_in_region_statistics, name='districts_in_region_statistic'),

]
