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

def types(request):
    type=product.objects.all()
    type2=[]
    for i in type:
         if i.type not in type2:
              type2.append(i.type)
    return type2
# Create your views here.
def index(request):
    data=product.objects.all()[::-1][:5]
    price=weight.objects.all()
    price2=filter(data,price)
    data2=product.objects.all()
    allp=filter(data2,price)
    data3=product.objects.all()[::-1][:3]
    addp=filter(data3,price)
    # type=product.objects.all()
    # type2=[]
    # for i in type:
    #      if i.type not in type2:
    #           type2.append(i.type)
    return render(request,'index.html',{'data':data,'price':price2,'allp':allp,'addp':addp,'user':getuser(request),'type':types(request)})

def products(request,pk):
    product1=product.objects.get(pk=pk)
    weights=weight.objects.filter(p_name=product1)
    data=product.objects.filter(type=product1.type)
    price=weight.objects.all()
    price2=filter(data,price)
    return render(request,'product_copy.html',{'weights':weights,'product1':product1,'user':getuser(request),'data':data,'price':price2,'type':types(request)})

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
        
            return redirect(login)
        else:
            return render(request,"login.html",{'type':types(request),'user':getuser(request)})
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
        if password==cnf_password:
            data=users.objects.create(name=name,phno=phno,email=email,username=username,password=password)
            data.save()
            messages.warning(request, "Password Doesn't match !")  # recorded
        else:
            messages.warning(request, "Account created successfully pls login to continue !")  # recorded
        

        return redirect(login)
    else:
        return render(request,"signup.html",{'type':types(request),'user':getuser(request)})

def catagory(request,type):
    data=product.objects.filter(type=type)
    price=weight.objects.all()
    price2=filter(data,price)
    return render(request,'catagory.html',{'data':data,'price':price2,'type':types(request),'user':getuser(request)})

def user(request):
    data=users.objects.get(username=request.session.get('user'))
    price=weight.objects.all()
    data2=product.objects.all()
    allp=filter(data2,price)
    return render(request,'user.html',{'allp':allp,'type':types(request),'user':getuser(request),'customer':data})

def yourorders(request):
     return render(request,'yourorders.html',{'type':types(request),'user':getuser(request)})

def address(request):
     data=users.objects.get(username=request.session.get('user'))
     adr=addreses.objects.filter(u_name=data.pk)
     return render(request,'address.html',{'type':types(request),'user':getuser(request),'customer':data,'adr':adr})

def add_address(request):
    if 'user' in request.session:
        data=users.objects.get(username=request.session.get('user'))
          
        if request.method=='POST':
               region=request.POST['region']
               fullname=request.POST['fullname']
               mobilenumber=request.POST['mobilenumber']
               pincode=request.POST['pincode']
               add1=request.POST['add1']
               add2=request.POST['add2']
               landmark=request.POST['landmark']
               town=request.POST['town']
               state=request.POST['state']
               data=addreses.objects.create(u_name=data,region=region,fullname=fullname,mobilenumber=mobilenumber,pincode=pincode,add1=add1,add2=add2,landmark=landmark,town=town,state=state)
               data.save()
               return redirect(address)

    else:
        return redirect(login)
    return render(request,'add_address.html',{'type':types(request),'user':getuser(request),'data':data})


def update_address(request,pk):
    if 'user' in request.session:
        data2=users.objects.get(username=request.session.get('user'))
        data1=addreses.objects.get(pk=pk)
        userdata=data1
        if request.method=='POST':
            region=request.POST['region']
            fullname=request.POST['fullname']
            mobilenumber=request.POST['mobilenumber']
            pincode=request.POST['pincode']
            add1=request.POST['add1']
            add2=request.POST['add2']
            landmark=request.POST['landmark']
            town=request.POST['town']
            state=request.POST['state']
            data=addreses.objects.filter(pk=pk).update(region=region,fullname=fullname,mobilenumber=mobilenumber,pincode=pincode,add1=add1,add2=add2,landmark=landmark,town=town,state=state)
            messages.success(request, "Address Successfully Updated!")
            return redirect(address)
            

        return render(request,'update_address.html',{'userdata':userdata})
    else:
         return redirect(login)
    
def remove_address(request,pk):
    if 'user' in request.session:
        addreses.objects.get(pk=pk).delete()
        messages.WARNING(request, "Address Deleted Successfully!!")
    return redirect(address)   
def cart(request):
     return render(request,'cart.html')

def update_user(request):
    if 'user' in request.session:
        data=users.objects.get(username=request.session.get('user'))
        if request.method=='POST':
            name=request.POST['name']
            phno=request.POST['phno']
            email=request.POST['email']
            username=request.POST['username']
            data=users.objects.filter(username=data.username).update(name=name,phno=phno,email=email,username=username)
            messages.success(request, "Personal Info Updated Successfully!")
            return redirect(update)
        
    return render(request,'update_user.html',{'data':data})

def update(request):
     
    return render(request,'update.html')

def update_password(request):
    if 'user' in request.session:
        data=users.objects.get(username=request.session.get('user'))
        if request.method=='POST':
            currentpassword=request.POST['currentpassword']
            newpassword=request.POST['newpassword']
            confirmpassword=request.POST['confirmpassword']
            try:
                data=users.objects.get(password=currentpassword)
                if newpassword==confirmpassword:
                    data=users.objects.filter(pk=data.pk).update(password=newpassword)
                    print(data)
                    messages.success(request, "Successfully changed password!!")
                else:
                    messages.warning(request, "Password Doesn't match!!")
            except:
                messages.warning(request, "Incorrect Password!")

    return render(request,'update_password.html')