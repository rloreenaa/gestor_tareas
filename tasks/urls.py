from django.urls import path
from . import views

urlpatterns = [
    path('lists/', views.task_lists),
    path('lists/<int:list_id>/', views.task_list_detail),
    path('lists/<int:list_id>/tasks/', views.tasks),
    path('lists/<int:list_id>/tasks/<int:task_id>/', views.task_detail),
]