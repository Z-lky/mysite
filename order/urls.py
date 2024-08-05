# @时间 2024/8/1 16:50
# @Author：郑摇2021210510
# @File : urls.py
from django.urls import path
from order import views

urlpatterns = [
    path('', views.AddOrderView.as_view()),
    path('order.html', views.OrderView.as_view()),
    # path('order_pay/', views.OrderPayView.as_view()),
    path('topay/', views.ToPayView.as_view()),
    path('checkPay/', views.checkPay),
    path('orderList/', views.OrderListView.as_view()),
    path('logistics/', views.LogisticsView.as_view()),

]
