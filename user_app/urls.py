from django.urls import path
from . import views

app_name = 'user_app'

urlpatterns = [
    path('details/<int:user_id>/', views.display_user_details_page, name='user_details'),
    path('register/', views.display_register_page, name='register'),
    path('login/', views.display_login_page, name='login'),
    path('logout/', views.display_logout_page, name='logout'),

]
