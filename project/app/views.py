from django.shortcuts import render,redirect
from.models import *
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
import bcrypt
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.conf import settings
import razorpay
import json
from django.urls import reverse

# from django.views.decorators.csrf import csrf_exempt

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

def search_func(request):
    if request.method=='POST':
        inp=request.POST['search']
        pro_name=[]
        data=product.objects.all()
        catago=[]
        for i in data:
            if i.name==inp:
                pro_name.append(i)
                catago.append(i.type)
            elif i.type==inp:   
                pro_name=product.objects.filter(type=inp)
        price=weight.objects.all()
        price2=filter(pro_name,price)
    return render(request,'search.html',{'price':price2,'type':types(request),'user':getuser(request)})
    



#Index
def index(request):
    data=product.objects.all()[::-1][:8]
    price=weight.objects.all()
    price2=filter(data,price)
    data2=product.objects.all()[:8]
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

def see_all(request):
    data=product.objects.all()
    price=weight.objects.all()
    price2=filter(data,price)
    return render(request,'see_all.html',{'price':price2})
        




#Login & Signup
def login(request):
   
        if request.method=="POST":
            username=request.POST['username']
            password=request.POST['password']
            psw=password.encode('utf-8')
            # salt=bcrypt.gensalt()               #Password Hashing
            # psw_hashed=bcrypt.hashpw(psw,salt)
            # print(psw_hashed)

            try:
                data=users.objects.get(username=username)
                if bcrypt.checkpw(psw,data.password.encode('utf-8')):
                    # data=users.objects.get(username=username,password=password.encode('utf-8'))
                    request.session['user']=username
                    messages.success(request, "Login successfully completed!") 
                else:
                    messages.warning(request, "Incorrect password!")
                

            except:
                messages.warning(request, "Incorrect Username!") 
        
            return redirect(login)
        else:
            return render(request,"login.html",{'type':types(request),'user':getuser(request)})
def logout(request):
    if getuser(request):
        del request.session['user']
        return redirect(login)
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

        psw=password.encode('utf-8')
        salt=bcrypt.gensalt()               #Password Hashing
        psw_hashed=bcrypt.hashpw(psw,salt)

        if password==cnf_password:
            data=users.objects.create(name=name,phno=phno,email=email,username=username,password=psw_hashed.decode('utf-8'))
            data.save()
            messages.success(request, "Account created successfully pls login to continue !")  # recorded
        else:
            messages.warning(request, "Password Doesn't match !")  # recorded
        

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
        int(data2)
        # item=cart_item.objects.get(pk=data2)
        # print(item.p_name_id)
        # amount=item.w_product.offer_price
        # name=data.name
        # print(amount)
        selected=0
        if pk:
            selected=int(pk)
        else:
            for i in adr:
                request.session['address']=i.pk
                selected=i.pk
        # # name='vysakh'
        # # amount = 3000
        # client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        # razorpay_order = client.order.create(
        #     {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        # )
        # order_id=razorpay_order['id']
        # order = Order.objects.create(
        #     name=name, amount=amount, provider_order_id=order_id
        # )
        # order.save()


        return render(request,'order_address.html',{'type':types(request),'user':getuser(request),'customer':data,'adr':adr,'selected':selected,'data2':data2,})
    else:
        return redirect(login)

def order_address1(request,pk):
    request.session['address']=pk
    return order_address(request,pk)


def payment(request,data2):
    request.session['prod']=data2
    print('user session created')
    if getuser(request):
        data=users.objects.get(username=request.session.get('user'))
        # name='vysakh'
        # amount = 3000
        int(data2)
        print(type(data2))
        
        item=cart_item.objects.get(pk=data2)
        print(item.p_name_id)
        amount=item.w_product.offer_price
        name=data.name
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order_id=razorpay_order['id']
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=order_id
        )
        order.save()
        return render(
            request,
            "index3.html",
            {
                "callback_url": "http://127.0.0.1:8000/" + "razorpay/callback/",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "order": order,
            },
            )

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
        st_exp_date=str(expected_date)
        expdate_obj=datetime.strptime(st_exp_date,"%Y-%m-%d")
        replacedt=expdate_obj + timedelta(days=7)
        replacing_date=replacedt.date()
        adr_item=addreses.objects.get(pk=request.session.get('address'))
        data=orders.objects.create(c_item=item,address_item=adr_item,ordered_date=formatted_date,expected_date=expected_date,replacing_date=replacing_date)
        data.save()


        user=users.objects.get(username=request.session.get('user'))
        email=user.email
        print(type(email))
        subject="Your Order has been successfully Placed"
        message = "Your Order "+item.p_name.name+" has been placed successfully. Product is expected on "+str(expected_date)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail( subject, message, email_from, recipient_list )

        messages.success(request,'Order Placed Check out your mail for more details!!')
        return redirect(view_cart)
    else:
        return redirect(login)
    
@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        print(client.utility.verify_payment_signature(response_data))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            # return render(request, "callback.html", context={"status": order.status})   # callback giving html page
            #  or  return redirect(function name of callback giving html page)
            print(request.session)
            print(product)
            return redirect(add_order)
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request,"index3.html", context={"status": order.status})  # callback giving html page
            #  or  return redirect(function name of callback giving html page)

    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "callback.html", context={"status": order.status})  # callback giving html page
        #  or  return redirect(function name of callback giving html page)

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

def replace_product(request):
    if getuser(request):
        username=request.session.get('user')
        user1=users.objects.get(username=username)
        cart_items=cart_item.objects.filter(uname=user1)
        x=datetime.now()
        date=(x.strftime("%x"))
        date_string = date
        parts = date_string.split("/")
        year = "20" + parts[2]
        formatted_date = f"{year}-{parts[0]}-{parts[1]}"
        date_obj = datetime.strptime(formatted_date, "%Y-%m-%d")
        date_obj1=date_obj.date()
        ordered_item=[]
        replaced_items=[]
        for i in cart_items:
            data1=orders.objects.filter(c_item=i.pk)
            if data1:
                ordered_item.append(data1)
        for j in ordered_item:
            for k in j:
                print(k.replacing_date)
                if k.delivered==True and k.replaced==False and date_obj1 <= k.replacing_date :
                    replaced_items.append(k)
        print(replaced_items)
                        
        price=[]
        for i in cart_items:
            of_p=i.w_product.offer_price
            count=i.quantity
            price.append({'id':i.pk,'price':of_p*count})
        return render(request,'replace_product.html',{'type':types(request),'user':getuser(request),'oritem':ordered_item,'price':price,'replaced_items':replaced_items})
    else:
        return redirect(login)
def replace_reorder(request,pk):
    reorder_item=orders.objects.get(pk=pk)
    reorder_item.replaced=True
    reorder_item.save()
    if reorder_item.delivered:
        x=datetime.now()
        date=(x.strftime("%x"))
        date_string = date
        parts = date_string.split("/")
        year = "20" + parts[2]
        formatted_date = f"{year}-{parts[0]}-{parts[1]}"
        date_obj = datetime.strptime(formatted_date, "%Y-%m-%d")
        expected = date_obj + timedelta(days=7)
        expected_date=expected.date()
        st_exp_date=str(expected_date)
        expdate_obj=datetime.strptime(st_exp_date,"%Y-%m-%d")
        replacedt=expdate_obj + timedelta(days=7)
        replacing_date=replacedt.date()


        data=orders.objects.create(c_item=reorder_item.c_item,address_item=reorder_item.address_item,payment=False,packed=False,shipped=False,outfordelivery=False,delivered=False,ordered_date=formatted_date,expected_date=expected_date,replacing_date=replacing_date)
        data.save()

    return redirect (replace_product)

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
def buyagain(request):
    if getuser(request):
            username=request.session.get('user')
            user1=users.objects.get(username=username)
            cart_items=cart_item.objects.filter(uname=user1)
            x=datetime.now()
            date=(x.strftime("%x"))
            date_string = date
            parts = date_string.split("/")
            year = "20" + parts[2]
            formatted_date = f"{year}-{parts[0]}-{parts[1]}"
            date_obj = datetime.strptime(formatted_date, "%Y-%m-%d")
            date_obj1=date_obj.date()
            ordered_item=[]
            names=[]
            singlename=[]
            buyagain_items=[]
            for i in cart_items:
                data1=orders.objects.filter(c_item=i.pk)
                if data1:
                    ordered_item.append(data1)
            for i in ordered_item:
                for j in i:
                    names.append(j.c_item.p_name.name)
            for i in names:
                if i not in singlename:
                    singlename.append(i)
            print(singlename)
            for i in singlename:
                data=product.objects.filter(name=i)
                price=weight.objects.all()
                price2=filter(data,price)
                for i in price2:
                    buyagain_items.append(i)
            return render(request,'buyagain.html',{'type':types(request),'user':getuser(request),'buyagain_items':buyagain_items})
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
            psw=currentpassword.encode('utf-8')
            psw2=newpassword.encode('utf-8')
            salt=bcrypt.gensalt()               #Password Hashing
            psw_hashed=bcrypt.hashpw(psw2,salt)
            try:
                if bcrypt.checkpw(psw,data.password.encode('utf-8')):
                    if newpassword==confirmpassword:
                        data=users.objects.filter(pk=data.pk).update(password=psw_hashed.decode('utf-8'))
                        # print(data)
                        messages.success(request, "Successfully changed password!!")
                    else:
                        messages.warning(request, "Password Doesn't match!!")
                else:
                    messages.warning(request,'Current password didnt match your account')
            except:
                messages.warning(request, "Incorrect Password!")

        return render(request,'update_password.html')
    else:
        return redirect(login)

def forgot_password_mail(request):
    if request.method=='POST':
        email=request.POST['email']
        subject='Change Password'
        path='http://127.0.0.1:8000/forgot_password'
        message = f"Click the Link below to change the password\n\n{path}\n\nPls login again using web to continue"
        email_from = settings.EMAIL_HOST_USER
        recipient_list= [email,]
        try:
            send_mail(subject,message,email_from,recipient_list)
            messages.success(request,"Email sent ! Check your inbox")
        except:
            messages.warning(request,"Error Pls try again with another Email")
    return render(request,'forgot_password_mail.html')





def forgot_password(request):
    if request.method=='POST':
        email=request.POST['email']
        new_password=request.POST['newpassword']
        conform_password=request.POST['confirmpassword']
        psw=new_password.encode('utf-8')
        salt=bcrypt.gensalt()               #Password Hashing
        psw_hashed=bcrypt.hashpw(psw,salt)
        if new_password==conform_password:
            try:
                data=users.objects.filter(email=email).update(password=psw_hashed.decode('utf-8'))
                print(data)
                messages.success(request,"Password Changed Sucessfully")
            except:
                messages.warning(request,"User assosiated to this mail does't exist")
        else:
                messages.warning(request, "Passwords Doesn't match!!")
        # print(email,new_password,conform_password)

    return render(request,'forgot_password.html')



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
    
