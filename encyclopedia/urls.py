from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.entry, name="entry"),
    path("query/", views.query, name="query"),
    path("add/", views.add, name="add"),
    path("edit/<str:name>", views.edit, name="edit"),
    path("randPage/", views.randPage, name="randPage"),
]
