from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'myapp'  # 名前空間を確認

urlpatterns = [
    path('country/create/', views.country_create, name='country_create'),   # 国の追加
    path('spot/list/', views.spot_list, name='spot_list'),                  # リストの表示(Home)
    path('spot/<int:pk>/update/', views.spot_update, name='spot_update'),   # 情報の更新
    path('spot/create/', views.spot_create, name='spot_create'),            # 観光地の追加
    path('spot/<int:pk>/delete/', views.spot_delete, name='spot_delete'),   # 削除ページのURL
    path('spot/<int:pk>/detail/', views.spot_detail, name='spot_detail'),   # 観光地の詳細
    path('spot/favorites/', views.is_favorite, name='is_favorite'),  # お気に入りページ
    path('spot/select/', views.calculate_overlapping_months, name='calculate_overlapping_months'),  # ベストシーズンの表示
    path('spot/<int:pk>/toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),  # お気に入り
    path('', views.spot_list, name='spot_list'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('mypage/', views.mypage, name='mypage'),
    path('mypage/update/', views.update_profile, name='update_profile'),
    path('myapp/login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),


]