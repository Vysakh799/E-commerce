from django.db import models

# Create your models here.
 
class product(models.Model):
    name=models.TextField()
    type=models.TextField()
    description=models.TextField()
    stock=models.TextField()
    image1=models.FileField()
    image2=models.FileField(null=True)
    image3=models.FileField(null=True)
    image4=models.FileField(null=True)
    
    def __str__(self):
        return self.name

class weight(models.Model):
    p_name=models.ForeignKey(product,on_delete=models.CASCADE)
    price=models.IntegerField()
    offer_price=models.IntegerField()
    weight=models.TextField(null=True)

    def __str__(self):
        return self.p_name.name

class users(models.Model):
    name=models.TextField()
    phno=models.IntegerField()
    email=models.EmailField()
    username=models.TextField()
    password=models.TextField()

    def __str__(self):
        return self.name

class addreses(models.Model):
    u_name=models.ForeignKey(users,on_delete=models.CASCADE)
    region=models.TextField()
    fullname=models.TextField()
    mobilenumber=models.TextField()
    pincode=models.TextField()
    add1=models.TextField()
    add2=models.TextField()
    landmark=models.TextField()
    town=models.TextField()
    state=models.TextField()

class contacts(models.Model):
    name=models.TextField()
    email=models.TextField()
    subject=models.TextField()
    description=models.TextField()

    def __str__(self):
        return self.name
class cart_item(models.Model):
    uname=models.ForeignKey(users,on_delete=models.CASCADE)
    p_name=models.ForeignKey(product,on_delete=models.CASCADE)
    w_product=models.ForeignKey(weight,on_delete=models.CASCADE)
    quantity=models.IntegerField()

class orders(models.Model):
    c_item=models.ForeignKey(cart_item,on_delete=models.CASCADE)
    address_item=models.ForeignKey(addreses,on_delete=models.CASCADE,null=True)
    payment=models.TextField(null=True)
    packed=models.BooleanField(default=False)
    shipped=models.BooleanField(default=False)
    outfordelivery=models.BooleanField(default=False)
    delivered=models.BooleanField(default=False)
    ordered_date=models.DateField(null=True)
    expected_date=models.DateField(null=True)

