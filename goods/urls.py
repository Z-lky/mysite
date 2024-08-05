# @时间 2024/7/11 下午3:55
# @File : urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('category_detail/<int:cid>/', views.CategoryDetailView.as_view()),
    path('goods_detail/<int:gid>/', views.GoodsDetailView.as_view()),
    path('goods_detail/<int:gid>/comment/', views.CommentView.as_view()),

]