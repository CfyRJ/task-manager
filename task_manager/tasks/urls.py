from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexSTasks.as_view(), name='index_tasks'),
    path('create/', views.CreateTask.as_view(), name='create_tasks'),
    path('<int:pk>/update/', views.UpdateTask.as_view(), name='update_tasks'),
    path('<int:pk>/delete/', views.DeleteTask.as_view(), name='delete_tasks'),
    path('<int:pk>/', views.ShowTask.as_view(), name='show_task'),
]
