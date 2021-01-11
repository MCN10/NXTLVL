from django.db import models
from django.utils.translation import gettext as _
from django.utils.text import slugify



# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=200, null=False)
    region = models.CharField(max_length=200, null=False)
    capital = models.CharField(max_length=200, null=False)
    latitude = models.DecimalField(_('Latitude'), max_digits=10, decimal_places=8)
    longitude = models.DecimalField(_('Longitude'), max_digits=11, decimal_places=8)    
    flag = models.ImageField(upload_to='main_product/', blank=True, null=False)
    culture = models.ImageField(upload_to='main_product/', blank=True, null=False)
    language = models.CharField(max_length=200, null=False)
    population = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'country'
        verbose_name_plural = 'countries'

    @property
    def flagURL(self):
        try:
            url = self.flag.url
        except:
            url = ''
        return url
    def cultureURL(self):
        try:
            url = self.culture.url
        except:
            url = ''
        return url


class Dish(models.Model):
    ## for product category
    dish_name = models.CharField(max_length=50, null=False, )
    slug = models.SlugField(blank=True, null=True)
    prep_time = models.CharField(max_length=50, null=False, )
    country = models.ForeignKey('Country' , on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=2000, null=False)
    images01 = models.ImageField(upload_to='main_product/', null=False)
    video = models.CharField(max_length=50, null=False, )

    def save(self , *args, **kwargs):
        if not self.slug and self.dish_name:
            self.slug = slugify(self.dish_name)
        super(Dish , self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'dish'
        verbose_name_plural = 'dishes'

    def __str__(self):
        return self.dish_name
    @property
    def image01(self):
        try:
            url = self.image1.url
        except:
            url = ''
        return url   


class Ingredient(models.Model):
    name = models.CharField(max_length=50, null=False, )
    image = models.ImageField(upload_to='main_product/', blank=True, null=False)
    dish = models.ForeignKey('Dish' , on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
