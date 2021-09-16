from django.urls import path
from . import views

app_name = "images"

urlpatterns = [
    path("detail/<int:id>/<slug:slug>/", views.image_detail, name="detail"),
]
