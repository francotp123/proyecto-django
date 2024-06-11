from django import forms
from influencers.models import Influencers

class CategoryForm(forms.Form):
    CATEGORY_CHOICES = [(category, category) for category in Influencers.objects.values_list('category', flat=True).distinct()]
    COUNTRY_CHOICES = [(country, country) for country in Influencers.objects.values_list('audience_country', flat=True).distinct()]
    COMPANY_SIZE_CHOICES = [
        ('large', 'Grande'),
        ('medium', 'Mediana'),
        ('small', 'Pequeña')
    ]

    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    company_size = forms.ChoiceField(choices=COMPANY_SIZE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    audience_country = forms.ChoiceField(choices=COUNTRY_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))