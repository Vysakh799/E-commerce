from django.shortcuts import render,redirect
from.models import *
from django.contrib import messages

def getuser(request):
    user=False

    if 'user' in request.session:
            user=True
    return user
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
    data2=product.objects.all()
    allp=filter(data2,price)
    data3=product.objects.all()[::-1][:3]
    addp=filter(data3,price)
    return render(request,'index.html',{'data':data,'price':price2,'allp':allp,'addp':addp,'user':getuser(request)})

def products(request,pk):
    product1=product.objects.get(pk=pk)
    weights=weight.objects.filter(p_name=product1)
    data=product.objects.filter(type=product1.type)
    price=weight.objects.all()
    price2=filter(data,price)
    return render(request,'product_copy.html',{'weights':weights,'product1':product1,'user':getuser(request),'data':data,'price':price2})

def login(request):
   
        if request.method=="POST":
            username=request.POST['username']
            password=request.POST['password']
            try:
                data=users.objects.get(username=username,password=password)
                request.session['user']=username
                messages.success(request, "Login successfully completed!") 

            except:
                messages.warning(request, "Incorrect username or password!") 
        
            return redirect(index)
        else:
            return render(request,"login.html")
def logout(request):
     del request.session['user']
     return redirect(index)
def signup(request):    
    if request.method=="POST":
        name=request.POST['name']
        phno=request.POST['phno']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        cnf_password=request.POST['cnf_password']
        
        data=users.objects.create(name=name,phno=phno,email=email,username=username,password=password,cnf_password=cnf_password)
        data.save()

        messages.warning(request, "Account created successfully pls login to continue !")  # recorded

        return redirect(login)
    else:
        return render(request,"signup.html")