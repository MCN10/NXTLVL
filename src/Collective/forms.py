from django.forms import ModelForm
from .models import *

class CollectiveOrderForm(ModelForm):
	class Meta:
		model = CollectiveOrder
		fields = '__all__'
		exclude = ['customer', 'transaction_id']


class CollectiveOrderItemsForm(ModelForm):
	class Meta:
		model = CollectiveOrderItem
		fields = '__all__'


class CollectiveShippingDetailsForm(ModelForm):
	class Meta:
		model = CollectiveShippingAddress	
		fields = '__all__'


class CollectiveProductsForm(ModelForm):
	class Meta:
		model = CollectiveProduct
		fields = '__all__'


class CollectiveCategoriesForm(ModelForm):
	class Meta:
		model = CollectiveCategory
		fields = '__all__'
		exclude = ['slug']

