from django.urls import path, include

from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'categories', views.CategoryViewset)
router.register(r'products', views.ProductViewSet)

urlpatterns = [
    path("", views.index, name="index"),
    path("api/", include(router.urls)),
    path("register/", views.register, name="register"),
    path("connect/", views.connect, name="connect"),
    path("logout/", views.logoutUser, name="logout"),
    path("login/", views.loginUser, name="login"),

]

