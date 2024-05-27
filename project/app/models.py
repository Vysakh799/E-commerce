from django.db import models

# Create your models here.
 
class product(models.Model):
    Name=models.TextField()
    type=models.TextField()
    price=models.TextField()
    offer_price=models.TextField()
    description=models.TextField()
    stock=models.TextField()
    weight1=models.TextField()
    weight2=models.TextField(null=True)
    weight3=models.TextField(null=True)
    weight4=models.TextField(null=True)
    weight5=models.TextField(null=True)
    image1=models.FileField()
    image2=models.FileField()
    image3=models.FileField()
    image4=models.FileField()
