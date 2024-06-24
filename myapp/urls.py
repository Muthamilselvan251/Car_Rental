from django.urls import path
from .views import success_view
# from .views import CustomPasswordResetView
from . import views
# from .views import total_price
from django.views.generic import TemplateView

urlpatterns =[
    path('',views.home,name="Home"),
    path('register/',views.register,name="register"),
    path('login/',views.loginpage,name="login"),
    path('booknow/',views.booknow,name="booknow"),
    path('rentcar/',views.rentcar,name="rentcar"),
    path('aboutus/',views.aboutus,name="aboutus"),
    path('contactus/',views.contactus,name="contactus"),
    path('success/', success_view, name='success_view'),
    path('forgot_password',views.forgot_password,name='forgot_password'),
    path('reset_password/<str:contact>/',views.reset_password,name='reset_password'),
    path('success/', TemplateView.as_view(template_name='success.html'), name='success'),
    path('error/', TemplateView.as_view(template_name='error.html'), name='error'),
    path('send_message/',views.send_message,name='send_message')

    # path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
]