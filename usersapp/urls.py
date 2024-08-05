# @时间 2024/7/22 11:26
# @Author：郑摇2021210510
# @File : urls.py

from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('checkUname/', views.CheckUnameView.as_view()),
    path('center/', views.CenterView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('loadCode.jpg', views.LoadCodeView.as_view()),
    path('checkcode/', views.CheckCodeView.as_view()),
    # 完善个人信息
    path('editPersonal/', views.EditPersonalView.as_view()),
    path('improve_personal/', views.ImprovePersonalView.as_view()),
    # 地址管理
    path('address/', views.AddressView.as_view()),
    path('loadArea/',  views.LoadAreaView.as_view()),
    path('address/edit/<int:aid>/', views.AddressEditView.as_view()),
    path('address/del/<int:aid>/', views.AddressDeleteView.as_view()),
    #发送验证码
    path('send_email_code/', views.email_code),
    path('checkEmail/', views.CheckEmailView.as_view()),
    path('checkEcode/', views.checkEcode.as_view()),
    # 忘记密码
    #搜索功能
    path('search_fuc/', views.SearchFucView.as_view()),
    #客服中心
    path('service/', views.ServiceView.as_view()),
    # 我的订单

]