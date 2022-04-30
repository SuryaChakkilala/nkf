from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.
class Food(models.Model):
    cat_choice = (
        ("Chinese", "Chinese"),
        ("Indian", "Indian"),
        ("Desserts", "Desserts"),
        ("Japanese", "Japanese"),
        ("Chat", "Chat"),
        ("Drinks", "Drinks"),
        ("Fast Food", "Fast Food")
    )
    
    name = models.TextField(default='_')
    price = models.FloatField(validators=[MinValueValidator(1)])
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    stock = models.IntegerField(default=0)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(default='-')
    healthy = models.BooleanField(default=False)
    vegetarian = models.BooleanField(default=True)
    category = models.TextField(choices=cat_choice)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url=''
        return url

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Cart'
        ordering = ['date_added']

    def __str__(self):
        return self.id

class CartItem(models.Model):
    item = models.ForeignKey(Food, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'CartItem'

    def sub_total(self):
        return self.item.price * self.quantity

    def __str__(self):
        return self.product

class Order(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='USD Order Total')
    emailAddress = models.EmailField(max_length=250, blank=True, verbose_name='Email Address')
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=250, blank=True)
    address = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=250, blank=True)
    postcode = models.CharField(max_length=250, blank=True)
    country = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    item = models.CharField(max_length=250)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def sub_total(self):
        return self.quantity * self.price

    def __str__(self):
        return self.item