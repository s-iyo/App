from django import forms
from .models import Spot, Country
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

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
    first_name = forms.CharField(max_length=30, label='名')
    last_name = forms.CharField(max_length=30, label='姓')
    email = forms.EmailField(label='メールアドレス')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')  # username を追加

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']  # 更新したいフィールド