from django.urls import path

from api.views import RegionListAPIView, DistrictListAPIView, MasjidListAPIView, MasjidDetailAPIView, \
    UserAPIView, PrayerTimeListAPIView, DistrictDetailAPIView
from namozvaqtlari.api import BugungiNamozVaqtiAPIView, NamozVaqtiAPIView, ClosestMasjidAPIView

urlpatterns = [
    path('user-create/', UserAPIView.as_view()),
    path('region-list/', RegionListAPIView.as_view()),
    path('district-list/', DistrictListAPIView.as_view()),
    path('district-detail/<int:pk>/', DistrictDetailAPIView.as_view()),
    path('mosque-list/', MasjidListAPIView.as_view()),
    path('prayer-list/', PrayerTimeListAPIView.as_view()),
    path('mosque-detail/<int:pk>/', MasjidDetailAPIView.as_view()),

    path('bugungi-namoz-vaqti', BugungiNamozVaqtiAPIView.as_view()),
    path('namoz-vaqtlari/', NamozVaqtiAPIView.as_view()),
    path('closest-masjids/', ClosestMasjidAPIView.as_view())
]
