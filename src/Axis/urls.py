from django.urls import path

from . import views

app_name = "Axis"


urlpatterns = [
    #Leave as empty string for base url

    #------------ (STORE - URLS) ------------

	path('', views.home, name="home"),
	path('store', views.store, name="store"),
    path('product_details/<str:pk>/', views.product_details, name="product_details"),
    path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('about/', views.about, name="about"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('contact/', views.contact, name="contact"),

    #------------ (STORE - Categories) ------------

    path('get_categorylayer2/', views.get_categorylayer2, name="categorylayer2"),
    path('get_categorylayer3/', views.get_categorylayer3, name="categorylayer3"),
    path('get_categorylayer4/', views.get_categorylayer4, name="categorylayer4"),
    path('get_categorylayer5/', views.get_categorylayer5, name="categorylayer5"),
    path('get_categorylayer6/', views.get_categorylayer6, name="categorylayer6"),

    
    #------------ (CRM - URLS) ------------
	path('dashboard', views.dashboard, name="dashboard"),
    path('customer/<str:pk>/', views.customer, name="customer"),
    path('shipping_details/<str:pk>/', views.shippingDetails, name="shipping_details"),

    #------------ (CRUD - Order - URLS) ------------
    path('create_order/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('order_details/<str:pk>/', views.viewOrder, name="view_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),


    #------------ (CRUD - Products - URLS) ------------
    path('products/', views.products, name="products"),
    path('add_product/', views.addProduct, name="add_product"),
    path('delete_product/<str:pk>/', views.deleteProduct, name="delete_product"),
    path('update_product/<str:pk>/', views.updateProduct, name="update_product"),

    #------------ (CRUD - Category - URLS) ------------
    path('categories/', views.categories, name="categories"),
    path('add_category/', views.addCategory, name="add_category"),
    path('delete_category/<str:pk>/', views.deleteCategory, name="delete_category"),
    path('update_category/<str:pk>/', views.updateCategory, name="update_category"),

]
