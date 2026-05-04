from django.contrib.auth.decorators import login_required # @login_required için şart
from .forms import UserUpdateForm # Az önce oluşturduğumuz formu içeri alıyoruz
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User # Django'nun hazır kullanıcı tablosu
from django.contrib import messages

from django.http import JsonResponse
from .models import Zone, Bike
from django.contrib.auth.decorators import login_required



@login_required
def reserve_view(request):
    zones = Zone.objects.all()
    return render(request, 'rentals/reserve.html', {'zones': zones})

@login_required
def get_bikes_api(request):
    zone_id = request.GET.get('zone_id')
    if zone_id:
        # Seçilen bölgedeki bisikletleri getir
        bikes = Bike.objects.filter(zone_id=zone_id).values('id', 'bike_number', 'bike_type', 'status')
        return JsonResponse({'bikes': list(bikes)})
    return JsonResponse({'error': 'Zone ID missing'}, status=400)

def signup_view(request):
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        # KONTROL: Bu kullanıcı adı daha önce alınmış mı?
        if User.objects.filter(username=u).exists():
            messages.error(request, "This username is already taken. Please choose another one.")
            return render(request, 'rentals/signup.html')
        
        # Eğer yoksa kaydet
        User.objects.create_user(username=u, password=p)
        messages.success(request, "Account created successfully! Now you can log in.")
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
            # Kullanıcı yoksa veya şifre yanlışsa mesaj ver
            messages.error(request, "User not found! Please sign up first.")
            
    return render(request, 'rentals/login.html')

def home(request):
    return render(request, 'rentals/home.html')

@login_required # Sadece giriş yapanlar görebilsin
def profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Hesabın başarıyla güncellendi!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'rentals/profile.html', {'form': form})