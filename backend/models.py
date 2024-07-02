from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 

#1-block
class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='nomi')
    price = models.IntegerField(verbose_name='narxi')
    case = models.IntegerField(default=1, verbose_name='yashikdagi soni')
    count = models.IntegerField(default=0, verbose_name='qoldiq')
    
    class Meta:
        verbose_name = 'maxsulot'
        verbose_name_plural = 'maxsulotlar'

    def total_price(self):
        return self.price * self.count * self.case

    def __str__(self):
        return f"{self.name}"

class InventoryProduct(models.Model):
    product = models.ForeignKey('Product', related_name='Product', on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='soni')
    inventory = models.ForeignKey('Inventory', related_name='Inventory', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'kirim(maxssulot)'
        verbose_name_plural = 'kirim(maxssulot)'

    def __str__(self):
        return f"{self.product}"

class Inventory(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'kirim'
        verbose_name_plural = 'kirim'

    def __str__(self):
        return f"{self.created_date}"

class Driver(models.Model):
    photo = models.ImageField(upload_to='images/', blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name='FIO')
    phone = models.CharField(max_length=255, verbose_name='Telefon')
    auto = models.CharField(max_length=255, verbose_name='Avtomobil')

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clientlar'

    def __str__(self):
        return self.name

class OrderProduct(models.Model):
    product = models.ForeignKey('Product', related_name='ProductFromOrder', on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='Narxi')
    count = models.IntegerField(verbose_name='soni')
    order = models.ForeignKey('Order', related_name='Order', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'chiqim(maxsulot)'
        verbose_name_plural = 'chiqim(maxsulot)'

    def __str__(self):
        return f"{self.product}"

class Order(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    driver = models.ForeignKey('Driver', related_name='Driver', on_delete=models.CASCADE)
    cash = models.IntegerField(default=0, verbose_name='Summa')


    class Meta:
        verbose_name = 'chiqim'
        verbose_name_plural = 'chiqim'

    def __str__(self):
        return f"{self.driver}-{self.created_date}"   

class Payment(models.Model):
    driver = models.ForeignKey('Driver', related_name='DriverForPayment', on_delete=models.CASCADE)
    cash = models.IntegerField(verbose_name='Summa')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.driver}'
#1-block

#2-block
class ConstructionSite(models.Model):
    name = models.CharField(max_length=255)
    

    def __str__(self):
        return self.name

class ConstructionSiteImage(models.Model):
    construction_site = models.ForeignKey(ConstructionSite, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='construction_site_images/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.construction_site.name}"

class ResponsiblePerson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    сonstruction_site = models.ForeignKey('ConstructionSite', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()

class Store(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    requisite = models.TextField(verbose_name='rekvizitlar')


    def __str__(self):
        return self.name

class PaymentRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    construction_site = models.ForeignKey(ConstructionSite, on_delete=models.CASCADE)
    responsible_person = models.ForeignKey(ResponsiblePerson, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_requests')

    def __str__(self):
        return f"Request {self.id} for {self.construction_site}"
#2-block
