from django.urls import path
from . import views

app_name = 'myapp'  # 名前空間を確認

urlpatterns = [
    path('spot/create/', views.spot_create, name='spot_create'),
    path('spot/<int:pk>/', views.spot_detail, name='spot_detail'),
    path('spot/<int:pk>/photo/', views.spot_photo, name='spot_photo'),
    path('country/create/', views.country_create, name='country_create'),  # 国作成ページのURLを追加
    path('spot/list/', views.spot_list, name='spot_list'),  # spot_list の URL パターンを追加
    path('spot/<int:pk>/update/', views.spot_update, name='spot_update'),  # spot_update の URL パターンを追加
]