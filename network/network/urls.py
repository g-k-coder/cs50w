
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('profile/<int:id>', views.profile_page, name="profile"),
    path('updateFollow/<str:action>/<int:user_id>/<int:follower_id>', views.updateFollow, name="update_follow"),
    path('followPosts/<int:id>', views.follow_posts, name='follow_posts'),
    path('edit/<str:action>/<int:id>', views.edit, name='edit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

