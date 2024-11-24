from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import book_accommodation
from .views import cancel_booking


urlpatterns = [
    path('register/', views.register, name='register'),
    path('index/', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    path('tours/', views.tours, name='tours'),
    path('accommodations/', views.accommodations, name='accommodations'),
    path('experiences/', views.experiences, name='experiences'),
    path('shahisnan/', views.shahisnan, name='shahisnan'),
    path('sample/', views.sample, name='sample'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('success/', views.success_view, name='success'),
    path('hotel1/', views.hotel1, name='hotel1'),
    path('hotel2/', views.hotel2 , name='hotel2'),
    path('hotel3/', views.hotel3 , name='hotel3'),
    path('hotel4/', views.hotel4 , name='hotel4'),
    path('hotel5/', views.hotel5 , name='hotel5'),
    path('hotel6/', views.hotel6 , name='hotel6'),

    # Booking URLs
    path('accommodations/<int:accommodation_id>/book/', views.book_accommodation, name='book_accommodation'),
    path('booking/success/<int:accommodation_id>/', views.booking_success, name='booking_success'),
    path('cancel_booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),

    # Custom Password Reset View
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    path('contacts/', views.contact_directory, name='contact_directory'),

    path('sos/', views.sos_button, name='sos_button'),
    path('sos/confirmation/', views.sos_confirmation, name='sos_confirmation'),
    path('lost-found/', views.lost_and_found, name='lost_and_found'),
    path('emergency-announcements/', views.emergency_announcements, name='emergency_announcements'),
    
]
