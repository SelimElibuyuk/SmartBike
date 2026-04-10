from django.contrib import admin
from django.urls import path
from rentals.views import home, login_view, signup_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),    
    path('signup/', signup_view, name='signup'),  
    path('dashboard/', home, name='home'),   
]