#views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import SpotForm, CountryForm
from collections import defaultdict
from .models import Spot, Tags, Month
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required



def spot_create(request):
    if request.method == 'POST':
        form = SpotForm(request.POST, request.FILES)
        if form.is_valid():
            spot = form.save()  # フォームを保存
            return redirect('myapp:spot_list')
        else:
            print(form.errors)  # フォームのエラーをコンソールに出力
    else:
        form = SpotForm()
    return render(request, 'myapp/spot_create.html', {'form': form, 'active_page': 'spot_create'})

def spot_detail(request, pk):
    spot = get_object_or_404(Spot, pk=pk)
    return render(request, 'myapp/spot_detail.html', {'spot': spot, 'active_page': 'spot_detail'}) # 必要に応じて

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

@login_required
def spot_list(request):
    selected_tags = request.GET.getlist('tag')
    selected_months = request.GET.getlist('month')

    spots_by_area = defaultdict(lambda: defaultdict(list))
    spots = Spot.objects.all().select_related('country__area')

    if selected_tags:
        spots = spots.filter(tag__id__in=selected_tags)

    if selected_months:
        spots = spots.filter(best_season__id__in=selected_months)

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


def toggle_favorite(request, pk):
    spot = get_object_or_404(Spot, pk=pk)
    spot.is_favorite = not spot.is_favorite
    spot.save()
    return JsonResponse({'is_favorite': spot.is_favorite})

def is_favorite(request):
    spots_by_area = defaultdict(lambda: defaultdict(list))
    # is_favoriteがTrueのスポットのみを取得
    spots = Spot.objects.filter(is_favorite=True).select_related('country__area')

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
        'active_page': 'is_favorite',  # active_pageを設定
    }
    return render(request, 'myapp/is_favorite.html', context)



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/myapp/spot/list/')  # 絶対パスを使用
    else:
        form = CustomUserCreationForm()
    return render(request, 'myapp/register.html', {'form': form})