from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import SpotForm, CountryForm
from .models import Spot

from django.shortcuts import render, redirect
from .forms import SpotForm

from django.shortcuts import render, redirect
from .forms import SpotForm
from .models import Spot, Area
from collections import defaultdict

def spot_create(request):
    if request.method == 'POST':
        form = SpotForm(request.POST)
        if form.is_valid():
            form.save()  # フォームのデータをデータベースに保存
            return redirect('myapp:spot_list')  # spot_list にリダイレクト
    else:
        form = SpotForm()
    return render(request, 'myapp/spot_create.html', {'form': form})

def spot_detail(request, pk):
    """
    特定の観光スポットの詳細を表示するビュー
    """
    spot = get_object_or_404(Spot, pk=pk)
    return render(request, 'myapp/spot_detail.html', {'spot': spot})

def spot_photo(request, pk):
    """
    観光スポットの画像を表示するビュー
    """
    spot = get_object_or_404(Spot, pk=pk)
    if spot.photo:
        return HttpResponse(spot.photo, content_type="image/jpeg")  # Content-Typeを設定
    else:
        return HttpResponse(status=404)  # 画像がない場合は404を返す

def country_create(request):
    """
    国を作成するビュー
    """
    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myapp:spot_create')  # 国の作成後に spot_create ページにリダイレクト
    else:
        form = CountryForm()
    return render(request, 'myapp/country_create.html', {'form': form})

def spot_list(request):
    spots_by_area = defaultdict(lambda: defaultdict(list))
    spots = Spot.objects.all().select_related('country__area')

    for spot in spots:
        area = spot.country.area
        country = spot.country
        spots_by_area[area][country].append(spot)

    # テンプレートで扱いやすい形式にデータを変換
    areas_data = []
    for area, countries in spots_by_area.items():
        countries_data = []
        for country, spots in countries.items():
            countries_data.append({
                'country': country,
                'spots': spots,
            })
        # 国名でソート
        countries_data.sort(key=lambda x: x['country'].name)
        areas_data.append({
            'area': area,
            'countries': countries_data,
        })

    # エリア名でソート
    areas_data.sort(key=lambda x: x['area'].name)

    context = {
        'areas_data': areas_data,
    }
    return render(request, 'myapp/spot_list.html', context)

def spot_update(request, pk):
    spot = get_object_or_404(Spot, pk=pk)
    if request.method == 'POST':
        form = SpotForm(request.POST, instance=spot)
        if form.is_valid():
            form.save()
            return redirect('myapp:spot_list')  # spot_list にリダイレクト
    else:
        form = SpotForm(instance=spot)
    return render(request, 'myapp/spot_update.html', {'form': form, 'spot': spot})