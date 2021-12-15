from django.urls import path,include
from . import views

urlpatterns = [
    path('create-parking-space/', views.Api_create_space, name="api-create-space"),
    path('parking-spaces/', views.Api_parking_space, name="api-parking-space"),
    path('update-parking-space/<str:pk>/', views.Api_update_parking_space, name="api-update-parking-space"),
    path('delete-parking-space/<str:pk>/', views.Api_delete_parking_space, name="api-delete-parking-space"),
    path('bookings/', views.Api_all_bookings, name="api-all-bookings"),
    path('book/<str:pk>/', views.Api_book_parking_space, name="api-book"),
    path('update-booking/<str:pk>/', views.Api_update_booking, name="api-update-booking"),
    path('cancel-booking/<str:pk>/', views.Api_cancel_booking, name="api-cancel-booking"),
    path('booking-detail/<str:pk>/', views.Api_get_booking_detail, name="api-booking-detail"),
]