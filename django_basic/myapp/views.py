from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .forms import SpotForm, CountryForm
from collections import defaultdict
from .models import Spot, Tags, Month, FavoriteSpot  # FavoriteSpot をインポート
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from .forms import UserProfileUpdateForm
from django.urls import reverse
from .forms import CustomUserCreationForm

def spot_create(request):
    if request.method == 'POST':
        form = SpotForm(request.POST, request.FILES)
        if form.is_valid():
            spot = form.save()
            return redirect('myapp:spot_list')
        else:
            print(form.errors)
    else:
        form = SpotForm()
    return render(request, 'myapp/spot_create.html', {'form': form, 'active_page': 'spot_create'})

def spot_detail(request, pk):
    spot = get_object_or_404(Spot, pk=pk)
    return render(request, 'myapp/spot_detail.html', {'spot': spot, 'active_page': 'spot_detail'})

def spot_photo(request, pk):
    spot = get_object_or_404(Spot, pk=pk)
    if spot.photo:
        return HttpResponse(spot.photo, content_type="image/jpeg")
    else:
        return HttpResponse(status=404)

def country_create(request):
    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myapp:spot_create')
    else:
        form = CountryForm()
    return render(request, 'myapp/country_create.html', {'form': form, 'active_page': 'country_create'})

def spot_list(request):
    selected_tags = request.GET.getlist('tag')
    selected_months = request.GET.getlist('month')

    spots_by_area = defaultdict(lambda: defaultdict(list))
    spots = Spot.objects.all().select_related('country__area')

    if selected_tags:
        spots = spots.filter(tag__id__in=selected_tags)

    if selected_months:
        spots = spots.filter(best_season__id__in=selected_months)

    # ログインしている場合、お気に入り情報を取得
    if request.user.is_authenticated:
        favorite_spots = FavoriteSpot.objects.filter(user=request.user).values_list('spot_id', flat=True)
    else:
        favorite_spots = []

    for spot in spots:
        area = spot.country.area
        country = spot.country
        # スポットがお気に入りかどうかを判定
        spot.is_favorite = spot.pk in favorite_spots
        spots_by_area[area][country].append(spot)

    areas_data = []
    for area, countries in spots_by_area.items():
        countries_data = []
        for country, spots in countries.items():
            countries_data.append({
                'country': country,
                'spots': spots,
            })
        countries_data.sort(key=lambda x: x['country'].name)
        areas_data.append({
            'area': area,
            'countries': countries_data,
        })

    areas_data.sort(key=lambda x: x['area'].name)

    tags = Tags.objects.all()
    months = Month.objects.all()

    context = {
        'areas_data': areas_data,
        'active_page': 'spot_list',
        'tags': tags,
        'months': months,
        'selected_tags': selected_tags,
        'selected_months': selected_months,
    }
    return render(request, 'myapp/spot_list.html', context)

def spot_update(request, pk):
    spot = get_object_or_404(Spot, pk=pk)
    if request.method == 'POST':
        form = SpotForm(request.POST, request.FILES, instance=spot)
        if form.is_valid():
            form.save()
            return redirect('myapp:spot_list')
    else:
        form = SpotForm(instance=spot)
    return render(request, 'myapp/spot_update.html', {'form': form, 'spot': spot, 'active_page': 'spot_update'})

def calculate_overlapping_months(request):
    if request.method == 'POST':
        selected_spot_ids = request.POST.getlist('selected_spots')
        selected_spots = Spot.objects.filter(pk__in=selected_spot_ids)
        best_seasons = [spot.best_season.all() for spot in selected_spots]

        if best_seasons:
            overlapping_months = set(best_seasons[0])
            for months in best_seasons[1:]:
                overlapping_months.intersection_update(months)
        else:
            overlapping_months = set()

        overlapping_months = sorted(list(overlapping_months), key=lambda month: month.number)

        context = {
            'overlapping_months': overlapping_months,
            'selected_spots': selected_spots,
            'active_page': 'calculate_overlapping_months',
        }
        return render(request, 'myapp/overlapping_months.html', context)
    else:
        spots_by_area = defaultdict(lambda: defaultdict(list))
        spots = Spot.objects.all().select_related('country__area')

        for spot in spots:
            area = spot.country.area
            country = spot.country
            spots_by_area[area][country].append(spot)

        areas_data = []
        for area, countries in spots_by_area.items():
            countries_data = []
            for country, spots in countries.items():
                countries_data.append({
                    'country': country,
                    'spots': spots,
                })
            countries_data.sort(key=lambda x: x['country'].name)
            areas_data.append({
                'area': area,
                'countries': countries_data,
            })

        areas_data.sort(key=lambda x: x['area'].name)

        context = {
            'areas_data': areas_data,
            'active_page': 'calculate_overlapping_months',
        }
        return render(request, 'myapp/select_spots.html', context)

def spot_delete(request, pk):
    spot = get_object_or_404(Spot, pk=pk)
    if request.method == 'POST':
        spot.delete()
        return redirect('myapp:spot_list')
    return render(request, 'myapp/spot_delete.html', {'spot': spot, 'active_page': 'spot_delete'})

@login_required  # ログイン必須にする
def toggle_favorite(request, pk):
    spot = get_object_or_404(Spot, pk=pk)
    try:
        favorite = FavoriteSpot.objects.get(user=request.user, spot=spot)
        favorite.delete()  # お気に入り解除
        is_favorite = False
    except FavoriteSpot.DoesNotExist:
        FavoriteSpot.objects.create(user=request.user, spot=spot)  # お気に入り登録
        is_favorite = True
    return JsonResponse({'is_favorite': is_favorite})

@login_required  # ログイン必須にする
def is_favorite(request):
    spots_by_area = defaultdict(lambda: defaultdict(list))
    # ログインユーザーのお気に入りスポットのみを取得
    favorite_spots = FavoriteSpot.objects.filter(user=request.user).select_related('spot', 'spot__country__area')

    for favorite in favorite_spots:
        spot = favorite.spot
        spot.is_favorite = True  # お気に入り状態をTrueに設定
        area = spot.country.area
        country = spot.country
        spots_by_area[area][country].append(spot)

    areas_data = []
    for area, countries in spots_by_area.items():
        countries_data = []
        for country, spots in countries.items():
            countries_data.append({
                'country': country,
                'spots': spots,
            })
        countries_data.sort(key=lambda x: x['country'].name)
        areas_data.append({
            'area': area,
            'countries': countries_data,
        })

    areas_data.sort(key=lambda x: x['area'].name)

    context = {
        'areas_data': areas_data,
        'active_page': 'is_favorite',
    }
    return render(request, 'myapp/is_favorite.html', context)

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            auth_login(request, user)
            return redirect(reverse('myapp:spot_list'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'myapp/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('myapp:spot_list')
            else:
                return render(request, 'myapp/login.html', {'form': form, 'error': 'ユーザー名またはパスワードが間違っています。'})
        else:
            return render(request, 'myapp/login.html', {'form': form, 'error': '入力内容に誤りがあります。'})
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect(reverse('myapp:login'))

@login_required
def mypage(request):
    user = request.user
    context = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }
    return render(request, 'myapp/mypage.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('myapp:mypage')
    else:
        form = UserProfileUpdateForm(instance=request.user)
    return render(request, 'myapp/update_profile.html', {'form': form})