from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max
from django.http import JsonResponse

from .forms import UserUpdateForm 
from .models import RentalsDemanddata, Zone, Bike

# --- Ana Sayfa ---
# rentals/views.py

def home(request):
    # Toplam bisiklet sayısı
    total_bikes = Bike.objects.count()
    
    # Müsait olanların sayısı
    available_bikes = Bike.objects.filter(status='available').count()
    
    # Veri setinden (1440 satırlık tablodan) ortalama sıcaklığı çekiyoruz
    avg_temp_data = RentalsDemanddata.objects.aggregate(Avg('temperature_c'))['temperature_c__avg']
    
    # Eğer veri yoksa 0 yazsın, varsa yuvarlasın
    avg_temp = round(avg_temp_data, 1) if avg_temp_data else 0

    context = {
        'total_bikes': total_bikes,
        'available_bikes': available_bikes,
        'avg_temp': avg_temp,
    }
    return render(request, 'rentals/home.html', context)

# --- Kayıt ve Giriş ---
def signup_view(request):
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        if User.objects.filter(username=u).exists():
            messages.error(request, "This username is already taken.")
            return render(request, 'rentals/signup.html')
        
        User.objects.create_user(username=u, password=p)
        messages.success(request, "Account created successfully! You can log in.")
        return redirect('login')
    return render(request, 'rentals/signup.html')

def login_view(request):
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "User not found or password incorrect!")
    return render(request, 'rentals/login.html')

# --- Rezervasyon Sayfası ---
@login_required
def reserve_view(request):
    # Veritabanındaki tüm bölgeleri çekip template'e gönderiyoruz
    zones = Zone.objects.all()
    return render(request, 'rentals/reserve.html', {'zones': zones})

# --- API: Seçilen Bölgeye Göre Bisikletleri Getir ---
@login_required
def get_bikes_api(request):
    zone_id = request.GET.get('zone_id')
    if zone_id:
        bikes = Bike.objects.filter(zone_id=zone_id).values('id', 'bike_number', 'bike_type', 'status')
        return JsonResponse({'bikes': list(bikes)})
    return JsonResponse({'error': 'Zone ID missing'}, status=400)

# --- Profil Güncelleme ---
@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hesabın başarıyla güncellendi!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'rentals/profile.html', {'form': form})

# --- Akıllı Analizler (Insights) ---
def insights_view(request):
    avg_demand = RentalsDemanddata.objects.aggregate(Avg('bike_demand'))['bike_demand__avg']
    max_demand = RentalsDemanddata.objects.aggregate(Max('bike_demand'))['bike_demand__max']
    avg_temp = RentalsDemanddata.objects.aggregate(Avg('temperature_c'))['temperature_c__avg']

    context = {
        'avg_demand': round(avg_demand, 2) if avg_demand else 0,
        'max_demand': max_demand if max_demand else 0,
        'avg_temp': round(avg_temp, 1) if avg_temp else 0,
    }
    return render(request, 'rentals/insights.html', context)
@login_required
def reserve_bike_action(request, bike_id):
    try:
        bike = Bike.objects.get(id=bike_id, status='available')
        bike.status = 'reserved' # Durumu güncelliyoruz
        bike.save()
        return JsonResponse({'status': 'success'})
    except Bike.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Bike not available'}, status=400)