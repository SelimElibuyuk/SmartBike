from django.contrib import admin
from django.urls import path
from rentals.views import home, login_view, signup_view, profile_view
from rentals import views  # <--- BURAYI DEĞİŞTİRDİK (nokta yerine rentals yazdık)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),    
    path('signup/', signup_view, name='signup'),  
    path('dashboard/', home, name='home'),   
    path('profile/', profile_view, name='profile'), 
    path('reserve/', views.reserve_view, name='reserve'), 
    path('api/get-bikes/', views.get_bikes_api, name='get_bikes_api'),
]