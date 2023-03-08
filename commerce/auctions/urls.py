from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.listing, {'user_id': None}, name="listing"),
    path("listing/<int:listing_id>/<int:user_id>", views.listing, name="listing"),
    path("create-listing/<int:user_id>", views.create_listing, name="create_listing"),
    path("watchlist/<int:user_id>", views.watchlist, name="watchlist"),
    path("category", views.category, {'category_name': None}, name="category"),
    path("category/<str:category_name>", views.category, name="category"),
    path("listings/<int:user_id>", views.user_listings, name="listings")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)