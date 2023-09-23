from django.urls import path,include
from .views import Welcome,StudentView,Admin_view
urlpatterns = [
    path('',Welcome,name='welcome page'),
    path('register/',StudentView.register,name='register page'),
    path('login/',StudentView.login,name='login page'),
    path('admin_register/',Admin_view.post_details,name='admin register page'),
    path('login/admin/',StudentView.get_details,)
]
