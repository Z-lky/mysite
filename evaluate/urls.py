# @时间 2024/8/5 10:31
# @Author：郑摇2021210510
# @File : urls.py
from django.urls import path
from evaluate import views


urlpatterns = [
    path('toAccess/', views.ToAccess.as_view()),
    path('addCommentOver/', views.AddCommentOver.as_view()),
    path('my_comments/', views.MyComments.as_view()),
    path('del_comments/', views.DelComments.as_view()),

]