from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.contrib import admin
from rentals.views import home, login_view, signup_view, profile_view
from rentals import views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),    
    path('signup/', signup_view, name='signup'),  
    path('dashboard/', home, name='home'),   
    path('profile/', profile_view, name='profile'), 
    path('reserve/', views.reserve_view, name='reserve'), 
    path('api/get-bikes/', views.get_bikes_api, name='get_bikes_api'),
    path('insights/', views.insights_view, name='insights'),
    path('api/reserve/<int:bike_id>/', views.reserve_bike_action, name='reserve_bike_action'),
    path('my-reservations/', views.my_reservations_view, name='my_reservations'),  # ← yeni
]