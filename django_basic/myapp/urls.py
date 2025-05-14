from django.urls import path
from . import views

app_name = 'myapp'  # 名前空間を確認

urlpatterns = [
    path('spot/create/', views.spot_create, name='spot_create'),
    path('country/create/', views.country_create, name='country_create'),   # 国の追加
    path('spot/list/', views.spot_list, name='spot_list'),                  # リストの表示(Home)
    path('spot/<int:pk>/update/', views.spot_update, name='spot_update'),   # 情報の更新
    path('spot/create/', views.spot_create, name='spot_create'),            # 観光地の追加
    path('spot/<int:pk>/delete/', views.spot_delete, name='spot_delete'),   # 削除ページのURL
    path('spot/select/', views.calculate_overlapping_months, name='calculate_overlapping_months'),  # ベストシーズンの表示
    
]