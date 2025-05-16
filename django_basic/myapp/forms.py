from django import forms
from .models import Spot, Country
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

class SpotForm(forms.ModelForm):
    class Meta:
        model = Spot
        fields = ['country', 'name', 'information', 'best_season', 'photo', 'tag']
        widgets = {
            'best_season': forms.CheckboxSelectMultiple,  # 複数選択をチェックボックスで表示
            'tag': forms.CheckboxSelectMultiple,  # 複数選択をチェックボックスで表示
        }

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['area', 'name']
        labels = {
            'area': 'エリア',
            'name': '国名'
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()  # Userモデルを指定
        fields = ('username', 'email', 'first_name', 'last_name')  # 表示するフィールド

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')

