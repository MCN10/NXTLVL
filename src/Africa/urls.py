from django.urls import path

from . import views

app_name = "Africa"


urlpatterns = [
    #Leave as empty string for base url
	path('', views.menu, name="menu"),
# 	path('cart/', views.cart, name="cart"),
# 	path('checkout/', views.checkout, name="checkout"),
# 	path('update_item/', views.updateItem, name="update_item"),
# 	path('process_order/', views.processOrder, name="process_order"),
# 	path('contact/', views.contact, name="contact"),

]
