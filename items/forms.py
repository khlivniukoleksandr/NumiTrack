from django import forms

from items.models import Collection


class CustomCollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ["name", "description", "cover"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control my-custom-class"}),
            "description": forms.Textarea(attrs={"class": "form-control my-custom-class"}),
            "cover": forms.ClearableFileInput(attrs={"class": "form-control-file"})
        }
