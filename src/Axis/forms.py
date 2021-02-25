from django.forms import ModelForm
from .models import *

class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = '__all__'
		exclude = ['customer', 'transaction_id']


class OrderItemsForm(ModelForm):
	class Meta:
		model = OrderItem
		fields = '__all__'


class ShippingDetailsForm(ModelForm):
	class Meta:
		model = ShippingAddress
		fields = '__all__'


class ProductsForm(ModelForm):
	class Meta:
		model = Product
		fields = '__all__'


class CategoriesForm(ModelForm):
	class Meta:
		model = Category
		fields = '__all__'
		exclude = ['slug']
        
class Categories2Form(ModelForm):
	class Meta:
		model = CategoryLayer2
		fields = '__all__'
		exclude = ['slug']
        
class Categories3Form(ModelForm):
	class Meta:
		model = CategoryLayer3
		fields = '__all__'
		exclude = ['slug']
        
class Categories4Form(ModelForm):
	class Meta:
		model = CategoryLayer4
		fields = '__all__'
		exclude = ['slug']
        
class Categories5Form(ModelForm):
	class Meta:
		model = CategoryLayer5
		fields = '__all__'
		exclude = ['slug']
        
class Categories6Form(ModelForm):
	class Meta:
		model = CategoryLayer6
		fields = '__all__'
		exclude = ['slug']
