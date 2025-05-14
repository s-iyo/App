from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import SpotForm, CountryForm
from .models import Spot
from collections import defaultdict

def spot_create(request):
    if request.method == 'POST':
        form = SpotForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('myapp:spot_list')
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

def spot_list(request):
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
        'active_page': 'spot_list',  # または 'home' など適切な名前
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