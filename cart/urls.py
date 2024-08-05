# @时间 2024/7/30 15:36
# @Author：郑摇2021210510
# @File : urls.py

from django.urls import path

from cart import views

urlpatterns = [
    path('addCart/', views.AddCartView.as_view()),
    path('cartList/', views.CartListView.as_view()),
]

