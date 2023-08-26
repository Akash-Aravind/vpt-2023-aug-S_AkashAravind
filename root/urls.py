from django.urls import path, include, re_path
from . import views
from django.views.static import serve
from django.conf import settings
app_name = "root"

urlpatterns=[
    path('', views.HomePage.as_view(), name="home"),
    path('search/', views.SearchPage, name="search"),
    path('details/<str:title>', views.DetailPage.as_view(), name="detail"),
    path('wishlist/<str:isbn>/<str:title>', views.Wishlist, name="wishlist"),
    path('wishlistview/', views.WishListView.as_view(), name="wishlistview"),
    path('wishlist/details/<str:title>/',views.DetailPage.as_view(),name="detail3"),
    path('wishlist/remove/<str:isbnum>/', views.removewishlist, name="remove"),
    path("register/", views.registerPage, name="register")


]