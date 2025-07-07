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
