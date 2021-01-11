from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models import Count
from django.conf import settings

# Create your models here.
class CollectiveCustomer(models.Model):
    User            = settings.AUTH_USER_MODEL
    user            = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email           = models.CharField(max_length=200, null=True)
    date_created    = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        if self.email:
            return self.email
    @property
    def orders(self):
        order_count = self.collectiveorder_set.all().count()
        return str(order_count)


class CollectiveProduct(models.Model):
    name        = models.CharField(max_length=200, null=False)
    description = models.TextField(max_length=2000, null=False)
    price       = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    image1      = models.ImageField(upload_to='collective_product/', blank=True, null=False)
    image2      = models.ImageField(upload_to='collective_product/', blank=True, null=False)
    image3      = models.ImageField(upload_to='collective_product/', blank=True, null=False)
    image4      = models.ImageField(upload_to='collective_product/', blank=True, null=False)
    category    = models.ForeignKey('CollectiveCategory' , on_delete=models.SET_NULL, null=True)
    price       = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    stock       = models.IntegerField(null=False)

    def __str__(self):
        return self.name

    @property
    def imageURL1(self):
        try:
            url = self.image1.url
        except:
            url = ''
        return url
    def imageURL2(self):
        try:
            url = self.image2.url
        except:
            url = ''
        return url
    def imageURL3(self):
        try:
            url = self.image3.url
        except:
            url = ''
        return url
    def imageURL4(self):
        try:
            url = self.image4.url
        except:
            url = ''
        return url


class CollectiveOrder(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Payment Confirmed, Processing Order', 'Payment Confirmed, Processing Order'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        ) 
    customer = models.ForeignKey(CollectiveCustomer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.customer.user.username)

    @property
    def collectiveshipping(self):
        collectiveshipping = True
        return collectiveshipping

    @property
    def get_cart_total(self):
        orderitems = self.collectiveorderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.collectiveorderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class CollectiveOrderItem(models.Model):
    product = models.ForeignKey(CollectiveProduct, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(CollectiveOrder, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class CollectiveShippingAddress(models.Model):
    customer        = models.ForeignKey(CollectiveCustomer, on_delete=models.SET_NULL, blank=True, null=True)
    order           = models.ForeignKey(CollectiveOrder, on_delete=models.SET_NULL, blank=True, null=True)
    country         = models.CharField(max_length=200, null=False)
    address1        = models.CharField(max_length=200, null=False)
    address2        = models.CharField(max_length=200, null=True)
    suburb          = models.CharField(max_length=200, null=True)
    city            = models.CharField(max_length=200, null=False)
    province        = models.CharField(max_length=200, null=False)
    postal_code     = models.CharField(max_length=20, null=False)
    date_added      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.customer.user.username)

class CollectiveCategory(models.Model):
    ## for product category
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, null=True)

    def save(self , *args, **kwargs):
        if not self.slug and self.category_name:
            self.slug = slugify(self.category_name)
        super(CollectiveCategory , self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'collective category'
        verbose_name_plural = 'collective categories'

    def __str__(self):
        return self.category_name


class CollectiveSize(models.Model):
    ## for product category
    size_name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, null=True)

    def save(self , *args, **kwargs):
        if not self.slug and self.size_name:
            self.slug = slugify(self.size_name)
        super(CollectiveSize , self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'collective size'
        verbose_name_plural = 'collective sizes'

    def __str__(self):
        return self.size_name


class CollectiveColor(models.Model):
    ## for product category
    color_name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, null=True)

    def save(self , *args, **kwargs):
        if not self.slug and self.color_name:
            self.slug = slugify(self.color_name)
        super(CollectiveColor , self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'collective color'
        verbose_name_plural = 'collective colors'

    def __str__(self):
        return self.color_name
