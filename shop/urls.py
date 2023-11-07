from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("products/<int:id>", views.ProductView, name="ProductView"),
    path("wishlist/", views.wishlist_view, name="wishlist"),
    path("cart/", views.cart_view, name="cart"),
    path("home/", views.home, name="home"),
    # path("search/", views.search, name="search"),
    path("login/", views.Login, name="login"),
    path('logout/',views.LogoutPage,name='logout'),
    path("signup/", views.signup, name="signup"),
    path('forget/',views.forget,name='forget'),
    path('search/',views.search,name='search'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('update_quantity/<int:product_id>/', views.update_quantity, name='update_quantity'),
    path('add_to_wish/<int:product_id>/', views.add_to_wish, name='add_to_wish'),
    path('delete_from_wishlist/<int:product_id>/', views.delete_from_wishlist, name='delete_from_wishlist'),
    path('move_all_to_cart/', views.move_all_to_cart, name='move_all_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
]
