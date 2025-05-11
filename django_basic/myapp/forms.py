from django import forms
from .models import Spot, Country

class SpotForm(forms.ModelForm):
    class Meta:
        model = Spot
        fields = ['country', 'name', 'information', 'best_season']  # photo を削除
        widgets = {
            'best_season': forms.CheckboxSelectMultiple,  # 複数選択をチェックボックスで表示
        }

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['area', 'name']