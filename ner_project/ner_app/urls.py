# ner_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.ner_view, name="ner_view"),
]
