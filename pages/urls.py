from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.registerPage, name='register'),
    path('menu/', views.menu, name='menu'),
    path('orders/', views.orders, name='orders'),
    path('account/', views.account, name='account'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:food_id>', views.add_cart, name='add_item'),
    path('cart/remove/<int:product_id>', views.cart_remove, name='cart_remove'),
    path('cart/remove_product/<int:product_id>', views.cart_remove_product, name='cart_remove_product'),    
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('menu/veg', views.vegetarian, name='veg'),
    path('menu/nonveg', views.nonvegetarian, name='nonveg'),
    path('search/', views.search, name='search'),
    path('recommendation_form/', views.recommendation_form, name='ml'),
    path('thanks/', views.thanks, name='thanks'),
    path('analytics/', views.analytics, name='analytics'),
    path('temp/', views.temp, name='temp')
]
