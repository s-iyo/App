from django import forms
from .models import Spot, Country
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SpotForm(forms.ModelForm):
    class Meta:
        model = Spot
        fields = ['country', 'name', 'information', 'best_season', 'photo', 'tag']
        widgets = {
            'best_season': forms.CheckboxSelectMultiple,  # 複数選択をチェックボックスで表示
            'tag': forms.CheckboxSelectMultiple,  # 複数選択をチェックボックスで表示
        }

        def clean(self):
            cleaned_data = super().clean()
            country = cleaned_data.get('country')
            name = cleaned_data.get('name')

            if country and name:
                existing_spot = Spot.objects.filter(country=country, name=name).exclude(pk=self.instance.pk).first()
                if existing_spot:
                    raise ValidationError("同じ国の同じ名前の観光地はすでに登録されています。")

            return cleaned_data

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['area', 'name']
        labels = {
            'area': 'エリア',
            'name': '国名'
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        area = self.cleaned_data.get('area')

        # 既存の国を検索
        existing_country = Country.objects.filter(area=area, name=name).exclude(pk=self.instance.pk).first()

        if existing_country:
            raise ValidationError("この国はすでに登録されています。")

        return name

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label='名')
    last_name = forms.CharField(max_length=30, label='姓')
    email = forms.EmailField(label='メールアドレス')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'email']