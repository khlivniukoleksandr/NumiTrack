from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from items.models import Collection, Coin, Banknote


class CustomCollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ["name", "description", "cover"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input"}),
            "description": forms.Textarea(attrs={"class": "form-input form-text-area"}),
            "cover": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
        }

class CustomCoinForm(forms.ModelForm):
    class Meta:
        model = Coin
        fields = ["name", "country", "year", "denomination", "material", "tirage", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input"}),
            "country": forms.TextInput(attrs={"class": "form-input"}),
            "year": forms.TextInput(attrs={"class": "form-input"}),
            "denomination": forms.TextInput(attrs={"class": "form-input"}),
            "material": forms.TextInput(attrs={"class": "form-input"}),
            "tirage": forms.TextInput(attrs={"class": "form-input"}),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-file-input",
                "data-initial-file-name": "django_placeholder"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        initial_name = ""
        if self.instance and self.instance.image:
            initial_name = getattr(self.instance.image, "public_id", "")

        self.fields['image'].widget.attrs['data-initial-file-name'] = initial_name


class CustomBanknoteForm(forms.ModelForm):
    class Meta:
        model = Banknote
        fields = ["name", "country", "year", "value", "tirage", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input"}),
            "country": forms.TextInput(attrs={"class": "form-input"}),
            "year": forms.TextInput(attrs={"class": "form-input"}),
            "value": forms.TextInput(attrs={"class": "form-input"}),
            "tirage": forms.TextInput(attrs={"class": "form-input"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-file-input",
                "data-initial-file-name": "django_placeholder"}),
        }


class CoinFilterForm(forms.Form):
    name = forms.CharField(required=False,
                              label="Name",
                              widget=forms.TextInput(attrs={"class":"form-coin-filter-input",
                                                                                            "placeholder":"Name"}))
    year = forms.IntegerField(required=False,
                              label="Year",
                              widget=forms.NumberInput(attrs={"class":"form-coin-filter-input",
                                                                                            "placeholder":"Year"}))
    country = forms.CharField(required=False, label="Country",
                              widget=forms.TextInput(attrs={"class":"form-coin-filter-input",
                                                            "placeholder":"Country"}))
    material = forms.CharField(required=False, label="Material",
                               widget=forms.TextInput(attrs={"class": "form-coin-filter-input",
                                                             "placeholder": "Material"}))

class CollectionFilterForm(forms.Form):
    name = forms.CharField(required=False,
                              label="Name",
                              widget=forms.TextInput(attrs={"class":"form-coin-filter-input",
                                                                                            "placeholder":"Name"}))
    description = forms.CharField(required=False, label="Description",
                              widget=forms.TextInput(attrs={"class":"form-coin-filter-input",
                                                            "placeholder":"Description"}))


class BanknoteFilterForm(forms.Form):
    name = forms.CharField(required=False,
                           label="Name",
                           widget=forms.TextInput(attrs={"class": "form-coin-filter-input",
                                                         "placeholder": "Name"}))
    year = forms.IntegerField(required=False,
                              label="Year",
                              widget=forms.NumberInput(attrs={"class": "form-coin-filter-input",
                                                              "placeholder": "Year"}))
    country = forms.CharField(required=False, label="Country",
                              widget=forms.TextInput(attrs={"class": "form-coin-filter-input",
                                                            "placeholder": "Country"}))


User = get_user_model()

class CollectorCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")