from django import forms
from LegalEaseHub_app.models import Case, ImageModel


class CasesForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['name', 'price', 'description', 'origin', 'number']


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ['image', 'title', 'price']




