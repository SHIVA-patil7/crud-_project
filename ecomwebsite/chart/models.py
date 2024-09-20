from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


# Create your models here.
class Customer(models.Model):

    user=models.OneToOneField(User,null=False,blank=False,on_delete=models.CASCADE)


    #extra fields
    phone_fields=models.CharField(max_length=12,blank=False)


def __str__(self):
    return self.user.username 


class Category(models.Model):
    category_name=models.CharField(max_length=200)
    def __str__(self):
        return self.category_name 
    

class Product(models.Model):
    name=models.CharField(max_length=100)
    category=models.ForeignKey('Category',on_delete=models.CASCADE)
    desc=models.TextField(default='default descriptions')
    price=models.FloatField(default=0.0)
    product_available_count=models.IntegerField(default=0)
    img=models.ImageField(upload_to='images/')


   # def get_add_to_cart_url(self):
        #return reverse("core:add-to-cart",
                       #kwargs={"pk":self.pk})
    

    def __str__(self):
        return self.name
    
    


class Order_Item(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    Ordered=models.BooleanField(default=False)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)


    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    
    def get_total_item_price(self):
        return self.quantity * self.product.price 
    
    def get_final_price(self):
        return self.get_total_item_price()
    


class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    items=models.ManyToManyField(Order_Item)
    start_date=models.DateTimeField(auto_now_add=True)
    Ordered_date=models.DateTimeField()
    Ordered=models.BooleanField(default=False)
    Order_id=models.CharField(max_length=100,unique=True,default=None,blank=True,null=True)
    datetime_ofpayment=models.DateTimeField(auto_now_add=True)
    Order_delivered=models.BooleanField(default=False)
    Order_recieved=models.BooleanField(default=False)






    def save(self,*args,**kwargs):
        if self.Order_id is None and self.datetime_ofpayment and self.id:
            self.Order_id = self.datetime_ofpayment.strftime("PAY2ME%Y%m%dODR")+ str(self.id)
        
        return super().save(*args,**kwargs)
    
    def __str__(self):
        return self.user.username 
    

    def get_total_price(self):
        total=0
        for Order_Item in self.items.all():
            total +=Order_Item.get_final_price()
        return total 
    

    def get_total_count(self):
        order=Order.objects.get(pk=self.pk)
        return order.items.count()
    
class CheckoutAddress(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    street_address=models.CharField(max_length=70)
    Apparment_address=models.CharField(max_length=90)
    country=CountryField(multiple=False,default='US')
    zip_code=models.CharField(max_length=70)


    def __str__(self):
        return self.user.username



