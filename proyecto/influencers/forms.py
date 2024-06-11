from django import forms
from influencers.models import Influencers

class CategoryForm(forms.Form):
    category = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = [(category, category) for category in Influencers.objects.values_list('category', flat=True).distinct()]