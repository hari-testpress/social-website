from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["title", "url", "description"]
        widgets = {"url": forms.HiddenInput}

    def clean_url(self):
        url = self.cleaned_data["url"]
        valid_extensions = ["jpg", "jpeg"]
        extention = url.split(".", 1)[1].lower()
        if extention not in valid_extensions:
            raise forms.ValidationError(
                "The given URL does not " "match valid image extensions."
            )
        return url

    def save(self, force_update=False, force_insert=False, commit=True):
        image_obj = super().save(commit=False)
        image_url = self.cleaned_data["url"]
        name = slugify(image_obj.title)
        extension = image_url.rsplit(".", 1)[1].lower()
        image_name = f"{name}.{extension}"
        response = request.urlopen(image_url)
        image_obj.image.save(image_name, ContentFile(response), save=False)
        if commit:
            image_obj.save()
        return image_obj
