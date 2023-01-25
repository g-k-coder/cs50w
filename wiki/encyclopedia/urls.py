from django.urls import path

from . import views

# Avoids namespace collision
app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name='entry'),
    path("new-page.html", views.newpage, name="newpage"),
    path("edit-page.html", views.editpage, name="editpage"),
    path("random-page.html", views.randompage, name="random")
]
