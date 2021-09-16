from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Image

# Create your views here.


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(
        request,
        "images/image/detail.html",
        {"section": "images", "image": image},
    )
