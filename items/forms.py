from django import forms

from items.models import Collection, Coin, Banknote


class CustomCollectionForm(forms.Form):
    name = forms.CharField(
        label="Collection Name",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        label="Description of Collection",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
    cover = forms.ImageField(
        label="Cover Image",
        required=False
    )
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)


