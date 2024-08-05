# @时间 2024/7/30 21:27
# @Author：郑摇2021210510
# @File : urls.py

from django.urls import path
from trend import views

urlpatterns = [
    path('trendList/', views.TrendView.as_view()),
]
