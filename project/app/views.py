from django.shortcuts import render,redirect
from.models import *
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt


#General functions
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




#Index
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





#Products Detailed Fuctions
def products(request,pk,pk1=None):
    if getuser(request):
        product1=product.objects.get(pk=pk)
        weights=weight.objects.filter(p_name=product1)
        user_name=users.objects.get(username=request.session.get("user"))
        # weights1=weight.objects.filter(p_name=product1).first
        # print(weights1)
        if pk1:
            selected=int(pk1)
            # print(request.session['weight'],'pk1',type(pk1))

        else:
            for i in weights[:1]:
                request.session['weight']=str(i.pk)
                selected=i.pk
            # print('pk2')
        data=product.objects.filter(type=product1.type)
        price=weight.objects.all()
        price2=filter(data,price)
        pk_item=False
        try:
            carted=cart_item.objects.filter(uname=user_name)
            for i in carted:
                if i.w_product.pk==int(request.session.get("weight")):
                    pk_item=True
                    break   
        except:
            pass




        # print(request.session['weight'])
        return render(request,'product.html',{'weights':weights,'product1':product1,'user':getuser(request),'data':data,'price':price2,'type':types(request),'selected':selected,'pk_item':pk_item})
    else:
        return redirect(login)

def products1(req,pk,pk1):
    # print(req.session['weight'])
    req.session['weight']=pk1
    return products(req,pk,pk1)






#Login & Signup
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
    if getuser(request):
        del request.session['user']
        return redirect(index)
    else:
        return redirect(login)
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





#catogary
def catagory(request,type):
    data=product.objects.filter(type=type)
    price=weight.objects.all()
    price2=filter(data,price)
    return render(request,'catagory.html',{'data':data,'price':price2,'type':types(request),'user':getuser(request)})







#Address Related Fuctions
def address(request):
    if getuser(request):
        data=users.objects.get(username=request.session.get('user'))
        adr=addreses.objects.filter(u_name=data.pk)
        return render(request,'address.html',{'type':types(request),'user':getuser(request),'customer':data,'adr':adr})
    else:
        return redirect(login)

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
        return render(request,'add_address.html',{'type':types(request),'user':getuser(request),'data':data})
        

    else:
        return redirect(login)


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
        messages.warning(request, "Address Deleted Successfully!!")
        return redirect(address)   
    else:
        return redirect(login)







#Cart Related Functions
def cart(request,pk):
    if getuser(request):
        user_data=users.objects.get(username=request.session.get('user'))
        # print(request.session['weight'])
        # print('Product',pk)
        data=cart_item.objects.create(uname=user_data,p_name=product.objects.get(pk=pk),w_product=weight.objects.get(pk=request.session.get('weight')),quantity='1')
        data.save()
        return redirect(view_cart)
    else:
        return redirect(login)

def view_cart(request):
    if getuser(request):
        user_data=users.objects.get(username=request.session.get('user'))
        data=cart_item.objects.filter(uname=user_data)
        price=[]
        total=0
        for i in data:
            of_p=i.w_product.offer_price
            count=i.quantity
            price.append({'id':i.pk,'price':of_p*count})
            total+=of_p*count

        return render(request,'cart.html',{'type':types(request),'user':getuser(request),'data':data,'price':price,'total':total})
    else:
        return redirect(login)

def delete_item(request,pk):
    cart_item.objects.get(pk=pk).delete()
    messages.warning(request, "Cart Item Deleted Successfully!!")
    return redirect(view_cart)
def incri_count(request,pk):
    prod=cart_item.objects.get(pk=pk)
    count=prod.quantity
    count+=1
    data=cart_item.objects.filter(pk=pk).update(quantity=count)
    return redirect(view_cart)
def decri_count(request,pk):
    prod=cart_item.objects.get(pk=pk)
    count=prod.quantity
    if count==1:
        pass
    else:
        count-=1
    data=cart_item.objects.filter(pk=pk).update(quantity=count)
    return redirect(view_cart)





#Order Related functions
def order_address(request,pk1,pk=None):
    if getuser(request):
        data=users.objects.get(username=request.session.get('user'))
        adr=addreses.objects.filter(u_name=data.pk)
        data2=pk1
        selected=0
        if pk:
            selected=int(pk)
        else:
            for i in adr:
                request.session['address']=i.pk
                selected=i.pk
        return render(request,'order_address.html',{'type':types(request),'user':getuser(request),'customer':data,'adr':adr,'selected':selected,'data2':data2})
    else:
        return redirect(login)

def order_address1(request,pk):
    request.session['address']=pk
    return order_address(request,pk)

def add_order(request,data2):
    if getuser(request):
        item=cart_item.objects.get(pk=data2)
        q=item.w_product.stock-item.quantity    #here the stock is decrimenting according to order
        weight.objects.filter(pk=item.w_product.pk).update(stock=q)
        # item.save()
        # print(item.w_product.stock)
        x=datetime.now()
        date=(x.strftime("%x"))
        date_string = date
        parts = date_string.split("/")
        year = "20" + parts[2]
        formatted_date = f"{year}-{parts[0]}-{parts[1]}"
        date_obj = datetime.strptime(formatted_date, "%Y-%m-%d")
        expected = date_obj + timedelta(days=7)
        expected_date=expected.date()
        adr_item=addreses.objects.get(pk=request.session.get('address'))
        data=orders.objects.create(c_item=item,address_item=adr_item,ordered_date=formatted_date,expected_date=expected_date)
        data.save()


        user=users.objects.get(username=request.session.get('user'))
        email=user.email
        print(type(email))
        subject="Your Order has been successfully Placed"
        message = "Your Order "+item.p_name.name+" has been placed successfully. Product is expected on "+str(expected_date)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail( subject, message, email_from, recipient_list )


        return redirect(view_cart)
    else:
        return redirect(login)


def add_order_address(request,data2):
    if 'user' in request.session:
        data=users.objects.get(username=request.session.get('user'))
        pk1=data2
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
               return order_address(request,pk1)
        return render(request,'add_order_address.html',{'type':types(request),'user':getuser(request),'data':data,'data2':data2})
    else:
        return redirect(login)


def update_order_address(request,pk,data2):
    if 'user' in request.session:
        data=users.objects.get(username=request.session.get('user'))
        data1=addreses.objects.get(pk=pk)
        userdata=data1
        pk1=data2
        # print(type(data2))
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
            data4=addreses.objects.filter(pk=pk).update(region=region,fullname=fullname,mobilenumber=mobilenumber,pincode=pincode,add1=add1,add2=add2,landmark=landmark,town=town,state=state)
            messages.success(request, "Address Successfully Updated!")
            return order_address(request,pk1)
        
        return render(request,'update_order_address.html',{'userdata':userdata,'data2':data2})
    else:
         return redirect(login)
    
def remove_order_address(request,pk,data2):
    if 'user' in request.session:
        pk1=data2
        addreses.objects.get(pk=pk).delete()
        messages.warning(request, "Address Deleted Successfully!!")
        return order_address(request,pk1)
    else:
        return redirect(login)


def track_order(request,pk):
    order=orders.objects.get(pk=pk)
    packed=order.packed
    shipped=order.shipped
    outfordelivery=order.outfordelivery
    delivered=order.delivered
    return render(request,'track_order.html',{'type':types(request),'user':getuser(request),'order':order,'packed':packed,'shipped':shipped,'outfordelivery':outfordelivery,'delivered':delivered})

def delete_order(request,pk):
    orders.objects.get(pk=pk).delete()
    return redirect (ordered_products)


def ordered_products(request):
    if getuser(request):
        username=request.session.get('user')
        user1=users.objects.get(username=username)
        cart_items=cart_item.objects.filter(uname=user1)
        ordered_item=[]

        for i in cart_items:
            data1=orders.objects.filter(c_item=i.pk)
            if data1:
                ordered_item.append(data1)
        price=[]
        for i in cart_items:
            of_p=i.w_product.offer_price
            count=i.quantity
            price.append({'id':i.pk,'price':of_p*count})
        return render(request,'ordered_products.html',{'type':types(request),'user':getuser(request),'oritem':ordered_item,'price':price})
    else:
        return redirect(login)

def return_product(request):
    if getuser(request):
        return render(request,'return_product.html')
    else:
        return redirect(login)


def buynow(request,pk):
    if getuser(request):
        user_data=users.objects.get(username=request.session.get('user'))
        # print(request.session['weight'])
        # print('Product',pk)
        data=cart_item.objects.create(uname=user_data,p_name=product.objects.get(pk=pk),w_product=weight.objects.get(pk=request.session.get('weight')),quantity='1')
        pk1=data.pk
        data.save()
        return order_address(request,pk1)
    else:
        return redirect(login)

def order_history(request):
    if getuser(request):
        username=request.session.get('user')
        user1=users.objects.get(username=username)
        cart_items=cart_item.objects.filter(uname=user1)
        ordered_item=[]
        for i in cart_items:
            data1=orders.objects.filter(c_item=i.pk)
            if data1:
                ordered_item.append(data1)
        return render(request,'order_history.html',{'type':types(request),'user':getuser(request),'oritem':ordered_item})
    else:
        return redirect(login)




#User Functions
def user(request):
    if getuser(request):
        data=users.objects.get(username=request.session.get('user'))
        price=weight.objects.all()
        data2=product.objects.all()
        allp=filter(data2,price)
        return render(request,'user.html',{'allp':allp,'type':types(request),'user':getuser(request),'customer':data})
    else:
        return redirect(login)

def yourorders(request):
    if getuser(request):
        return render(request,'yourorders.html',{'type':types(request),'user':getuser(request)})
    else:
        return redirect(login)
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
    else:
        return redirect(login)

def update(request):
    if getuser(request):
        return render(request,'update.html',{'type':types(request),'user':getuser(request)})
    else:
        return redirect(login)

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
                    # print(data)
                    messages.success(request, "Successfully changed password!!")
                else:
                    messages.warning(request, "Password Doesn't match!!")
            except:
                messages.warning(request, "Incorrect Password!")

        return render(request,'update_password.html')
    else:
        return redirect(login)




#Contact Function
def contact(request):
    if 'user' in request.session:
        if request.method=="POST":
            name=request.POST['name']
            email=request.POST['email']
            subject=request.POST['subject']
            description=request.POST['description']
            data=contacts.objects.create(name=name,email=email,subject=subject,description=description)
            data.save()
            messages.success(request, "OK our team will contact you as soon as possible !!")

            message = f"{description}\n\nName: {name}\n\nEmail: {email}\n\n!! CONTACT CUSTOMER AS FAST AS YOU CAN !!"
            email_from = settings.EMAIL_HOST_USER
            recipient_list= ["universal7995@gmail.com",]
            send_mail(subject,message,email_from,recipient_list)
        return render(request,'contact.html',{'type':types(request),'user':getuser(request)}) 
    else:
        return redirect(login)
    
# def send_custom_mail(subject,messege,sender_name,sender_email,recipient_list):
#     email_body=f"{messege}\n\nName:{sender_name}\n\nEmail:{sender_email}"
#     send_mail(
#         subject,
#         email_body,
#         settings.EMAIL_HOST_USER,
#         recipient_list,
#         fail_silently=False,
#     )
#     return redirect(contact)