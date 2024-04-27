from django.urls import path

from namozvaqtlari.api import BugungiNamozVaqtiAPIView, NamozVaqtiAPIView, ClosestMasjidAPIView

urlpatterns = [
    path('bugungi-namoz-vaqti', BugungiNamozVaqtiAPIView.as_view()),
    path('namoz-vaqtlari/', NamozVaqtiAPIView.as_view()),
    path('closest-masjids/', ClosestMasjidAPIView.as_view())
]
