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
    price=models.TextField()
    offer_price=models.TextField()
    weight=models.TextField(null=True)

    def __str__(self):
        return self.p_name.name
