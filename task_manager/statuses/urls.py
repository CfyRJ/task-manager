from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexStatuses.as_view(), name='index_statuses'),
    path('create/', views.CreateStatuse.as_view(), name='create_statuse'),
    path('<int:pk>/update/', views.UpdateStatuse.as_view(), name='update_statuse'),
    path('<int:pk>/delete/', views.DeleteStatuse.as_view(), name='delete_statuse'),
]
