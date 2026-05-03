
from django.contrib import admin
from django.urls import path
from rentals.views import home, login_view, signup_view, profile_view # profile_view'ı buraya ekledik

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),    
    path('signup/', signup_view, name='signup'),  
    path('dashboard/', home, name='home'),   
    path('profile/', profile_view, name='profile'), # "views." kısmını sildik çünkü direkt fonksiyonu import ettik
]