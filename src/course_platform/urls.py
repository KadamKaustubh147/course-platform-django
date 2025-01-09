from django.urls import path, include
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    # path('courses/', views.courses, name='courses'),
    path('', views.course_list_view, name='courses'),
    path('<slug:course_id>', views.course_detail_view, name='course_detail'),
    path('<slug:course_id>/lessons/<slug:lesson_id>/', views.lesson_detail_view, name='lesson_detail'),
]