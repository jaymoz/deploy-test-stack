from django.urls import path, include
from .  import views

urlpatterns = [
    path('', views.home, name="home"),
    path('booking/<str:pk>/', views.booking, name="booking"),
    path('parking-spaces/', views.get_parking_spaces, name="parking-spaces"),
    path('edit/booking/<str:pk>/', views.edit_booking, name="edit-booking"),
    path('cancel-booking/<str:pk>/', views.cancel_booking, name='cancel'),
    path('add-space/', views.add_parking_space, name="add-space"),
    path('update-space/<str:pk>/', views.update_parking_space, name="update-space"),
    path('delete-space/<str:pk>/', views.delete_parking_space, name="delete-space"),

]