# @时间 2024/8/2 17:59
# @Author：郑摇2021210510
# @File : urls.py
from django.urls import path, include
from forum import views

urlpatterns = [
    path('essay/', views.EssayListView.as_view()),
    path('essay_write/', views.EssayWriteView.as_view()),
    path('edit_over/', views.EssayEditView.as_view()),
    path('consultation/', views.ConsultationListView.as_view()),
    path('consultation_delete/', views.ConsultationDeleteView.as_view()),
]
