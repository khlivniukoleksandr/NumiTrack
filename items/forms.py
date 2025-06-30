from django import forms

from items.models import Collection, Coin, Banknote


class CustomCollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ["name", "description", "cover"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control my-custom-class"}),
            "description": forms.Textarea(attrs={"class": "form-control my-custom-class"}),
            "cover": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
        }

class CustomCoinForm(forms.ModelForm):
    class Meta:
        model = Coin
        fields = ["name", "country", "year", "denomination", "material", "tirage", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control my-custom-class"}),
            "country": forms.TextInput(attrs={"class": "form-control my-custom-class"}),
            "year": forms.TextInput(attrs={"class": "form-control my-custom-class"}),
            "denomination": forms.TextInput(attrs={"class": "form-control my-custom-class"}),
            "material": forms.TextInput(attrs={"class": "form-control my-custom-class"}),
            "tirage": forms.TextInput(attrs={"class": "form-control my-custom-class"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
        }


class CustomBanknoteForm(forms.ModelForm):
    class Meta:
        model = Banknote
        fields = ["name", "country", "year", "value", "tirage", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control my-custom-class"}),
            "country": forms.TextInput(attrs={"class": "form-control my-custom-class"}),
            "year": forms.TextInput(attrs={"class": "form-control my-custom-class"}),
            "value": forms.TextInput(attrs={"class": "form-control my-custom-class"}),
            "tirage": forms.TextInput(attrs={"class": "form-control my-custom-class"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
        }