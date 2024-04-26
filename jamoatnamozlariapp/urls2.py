from django.urls import path

from namozvaqtlari.api import BugungiNamozVaqtiAPIView, NamozVaqtiAPIView

urlpatterns = [
    path('bugungi-namoz-vaqti', BugungiNamozVaqtiAPIView.as_view()),
    path('namoz-vaqtlari/', NamozVaqtiAPIView.as_view())
]
