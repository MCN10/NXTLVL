import django_filters
from .models import *



class CollectiveOrderFilter(django_filters.FilterSet):
	class Meta:
		model = CollectiveOrder
		fields = '__all__'
		exclude = ['customer', 'date_created']

class CollectiveProductFilter(django_filters.FilterSet):
	class Meta:
		model = CollectiveProduct
		fields = ['name', 'category']

class CollectiveCategoryFilter(django_filters.FilterSet):
	class Meta:
		model = CollectiveCategory
		fields = ['category_name']
