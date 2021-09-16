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
        extention = url.rsplit(".", 1)[1].lower()
        if extention not in valid_extensions:
            raise forms.ValidationError(
                "The given URL does not " "match valid image extensions."
            )
        return url

    def save(self, force_update=False, force_insert=False, commit=True):
        image_obj = super().save(commit=False)
        self.image_url = self.cleaned_data["url"]
        image_name = self.get_image_name(image_obj)
        image = self.get_image()
        image_obj.image.save(image_name, image, save=False)
        if commit:
            image_obj.save()
        return image_obj

    def get_image(self):
        response = request.urlopen(self.image_url)
        return ContentFile(response.read())

    def get_image_name(self, image_obj):
        name = slugify(image_obj.title)
        extension = self.image_url.rsplit(".", 1)[1].lower()
        return f"{name}.{extension}"
