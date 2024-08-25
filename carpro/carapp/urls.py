from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('car_single/<int:id>/', views.car_single, name='car_single'),
    path('car_single/', views.car_single, name='car_single'),
    path('car/', views.car, name='car'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('pricing/', views.pricing, name='pricing'),
    path('signup', views.signup, name='signup'),
    path('login_page/', views.login_page, name='login_page'),
    path('about', views.about, name='about'),

    path('book_now/<int:car_id>/', views.book_now, name='book_now'),
#    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('booksuccess/', views.booksuccess, name='booksuccess'),
    path('payment/', views.payment, name='payment'),


    path('paylist', views.paylist, name='paylist'),
    path('logout_page', views.logout_page, name='logout_page'),



]