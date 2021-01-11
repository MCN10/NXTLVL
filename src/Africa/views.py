from django.shortcuts import render
from . models import *


# Create your views here.
def menu(request, category_slug=None):

	template = 'Africa/menu.html'

	countries = Country.objects.all()

	dishes = Dish.objects.all()

	ingredients= Ingredient.objects.all()

	context = {'countries':countries, 'dishes': dishes, 'ingredients': ingredients}

	return render(request, template, context)


