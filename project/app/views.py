from django.shortcuts import render
from.models import *


def filter(data,price):
    price2=[]
    for i in data:
        for j in price:
            if i.pk==j.p_name.pk:
                price2.append(j)
                break
    return price2
# Create your views here.
def index(request):
    data=product.objects.all()[::-1][:5]
    price=weight.objects.all()
    price2=filter(data,price)
    data2=product.objects.all()[:5]
    allp=filter(data2,price)
    data3=product.objects.all()[::-1][:3]
    addp=filter(data3,price)
    return render(request,'index.html',{'data':data,'price':price2,'allp':allp,'addp':addp})

def products(request,pk):
    product1=product.objects.get(pk=pk)
    weights=weight.objects.filter(p_name=product1)
    return render(request,'product.html',{'weights':weights,'product1':product1})