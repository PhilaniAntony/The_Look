from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#Client  model
class Client(models.Model):
    user = models.OneToOneField(User, null =True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null =  True)
    phone = models.CharField(max_length=200, null =  True)
    email= models.CharField(max_length=200, null =  True)
    date_created = models.DateTimeField(auto_now_add = True, null =  True)
    image = models.ImageField( null=True, blank= True)
    
    #Dispaly client by name on dashboard
    def __str__(self):
        return self.name
    
    #This method covers for thr error that occurs when you delete an image 
    #making the image.url an emty string 
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
#Client base of operation
class Address(models.Model):
    name = models.CharField(max_length=200, null =  True)
    block = models.CharField(max_length=200, null =  True)
    city = models.CharField(max_length=200, null =  True)
    state = models.CharField(max_length=200, null =  True)
    country = models.CharField(max_length=200, null =  True)
    zipcode = models.CharField(max_length=10, null =  True)
    
    #Display address by block 
    def __str__(self):
        return self.block
    
    
class Collection(models.Model) :
    STATUS =(
        ('Active', 'Active'),
        ('Deactived', 'Deactived'),
    )
    name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=450, null=True)
    status = models.CharField(max_length=200, null =  True, choices = STATUS)
    image = models.ImageField( null=True, blank= True)
    
    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
#category, collection, tag & product declareed in store will be moved to dashboard models.py 
class Category(models.Model):
    #Option to pause and activate a category in the shop
    STATUS =(
        ('Active', 'Active'),
        ('Paused', 'Paused'),
    )
    name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=450, null=True)
    status = models.CharField(max_length=200, null =  True, choices = STATUS)
    image = models.ImageField( null=True, blank= True)
    
    #Display cat by name
    def __str__(self):
        return self.name
    
    #image handling method 
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Tag(models.Model) :
    name = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name
    
#Payment Method
class Paymentmethod(models.Model) :
    name = models.CharField(max_length= 200, null = False)
    value = models.FloatField(null= True)
    date_added = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length= 200, null = False)
    
    def __str__(self):
        return self.name 
    
#Product model
class Product(models.Model):
    STATUS =(
        ('Active', 'Active'),
        ('Deactived', 'Deactived'),
    )
    SIZE =(
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        
    )
    name = models.CharField(max_length=200, null =  True)
    vendor = models.CharField(max_length=200, null =  True)
    productType = models.CharField(max_length=200, null =  True)
    description = models.CharField(max_length=400, null =  True, blank = True)
    date_created = models.DateTimeField(auto_now_add = True, null =  True)
   
    quantity = models.IntegerField(default=0)
    size = models.CharField(max_length=200, null =  True, choices = SIZE)
    color = models.CharField(max_length=200, null =  True)
    note = models.CharField(max_length=450, blank = True )
    
    unitPrice = models.FloatField(null= True)
    discount = models.FloatField(null= True)
    image = models.ImageField(null=True, blank=True)
    hs = models.CharField(max_length=200, null =  True)
    digital = models.BooleanField(default=False,null=True, blank=True)
    
    status = models.CharField(max_length=200, null =  True, choices = STATUS)
    category = models.ManyToManyField(Category)
    collection = models.ManyToManyField(Collection)
    tags = models.ManyToManyField(Tag)
    
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    @property
    def productPrice(self):
        if self.discount :
            price = self.productPrice - self.discount
            return price
        

class Supplier(models.Model):
    STATUS =(
        ('Active', 'Active'),
        ('Deactived', 'Deactived'),
    )
       
    name = models.CharField(max_length=200, null=False)
    account_manager = models.CharField(max_length=200, null=False)
    email = models.EmailField(max_length=200, null=False)
    phone = models.CharField(max_length=200, null=False)
    note = models.CharField(max_length=200, null =  True)
    
    address = models.CharField(max_length=450, null =  True)
    url = models.CharField(max_length=200, null =  True)
    image = models.ImageField( null=True, blank= True)
    
    #product
    product = models.ManyToManyField(Product)
    status = models.CharField(max_length=200, null =  True, choices = STATUS) 
    
    def __str__(self):
        return self.name
    
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
#Shipping Company
class Shipping_company(models.Model):
    STATUS =(
        ('Active', 'Active'),
        ('Deactived', 'Deactived'),
    )
    
    name = models.CharField(max_length=200, null=False)
    account_manager = models.CharField(max_length=200, null=False)
    email = models.EmailField(max_length=200, null=False)
    phone = models.CharField(max_length=200, null=False)
    url = models.CharField(max_length=200, null =  True)
    note = models.CharField(max_length=200, null =  True)
    image = models.ImageField( null=True, blank= True)
    
    #Order = models.ManyToManyField(Order)
    #address = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=200, null =  True, choices = STATUS)
    paymentmethod = models.ManyToManyField(Paymentmethod)

    
    def __str__(self):
        return self.name
    
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
   