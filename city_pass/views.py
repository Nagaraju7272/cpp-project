from django.shortcuts import render, redirect, HttpResponse
from app.EmailBackEnd import EmailBackEnd
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from app.models import CustomUser, Category, Passes, Page
from django.contrib.auth import get_user_model
import random
from django.core.paginator import Paginator

from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import make_aware
from datetime import datetime
User = get_user_model()


import boto3


def s3_bucket_upload_img(file_obj, object_name=None):
    bucket_name = "s3-cpp-x23423625"
    
    if object_name is None:
        object_name = file_obj.name  

    s3_client = boto3.client('s3')
    try:
        s3_client.upload_fileobj(file_obj, bucket_name, object_name)  
        print(f"File '{file_obj.name}' uploaded successfully to '{bucket_name}/{object_name}'")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False



def sns_email_send(subject, message):
    SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:008139402425:mysns-cpp-x23423625"
    
    try:
        sns_client = boto3.client("sns", region_name="us-east-1")
        response = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject=subject
        )
        print(f"Email sent successfully! Message ID: {response['MessageId']}")
        return True  
    except Exception as e:
        print(f"Error sending email: {e}")
        return False 



import requests

def send_email_api(subject, message, email):
    """
    Send an email using the API Gateway URL that triggers the Lambda function.
    """
    API_URL = "https://qv4edshm24.execute-api.us-east-1.amazonaws.com/mystage/lambda-cpp-x23423625"

    # Prepare the payload
    payload = {
        "subject": subject,
        "message": message,
        "email": email
    }

    try:
        # Send POST request to the API
        response = requests.post(API_URL, json=payload, headers={"Content-Type": "application/json"})

        # Check for a successful response
        if response.status_code == 200:
            data = response.json()
            print(f"Email API Response: {data}")
            return data.get("message", "No response message")
        else:
            print(f"Error: API returned status {response.status_code}")
            return None
    except Exception as e:
        print(f"Error while sending email via API: {str(e)}")
        return None


##########################################################

def BASE(request):
    return render(request, 'base.html')


def LOGIN(request):
    return render(request, 'login.html')


def doLogin(request):
    if request.method == 'POST':
        user = EmailBackEnd.authenticate(request,
                                         username=request.POST.get('email'),
                                         password=request.POST.get('password')
                                         )
        if user != None:
            login(request, user)
            return redirect('dashboard')

        else:
            messages.error(request, 'Email or Password is not valid')
            return redirect('login')
    else:
        messages.error(request, 'Email or Password is not valid')
        return redirect('login')


def doLogout(request):
    logout(request)
    return redirect('login')


def LANDINGPAGE(request):
    page = Page.objects.all()
    context = {'page': page,

               }

    return render(request, 'landingpage.html', context)


@login_required(login_url='/')
def DASHBOARD(request):
    end_date = timezone.now()
    #end_date = make_aware(datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S"))

    start_date = end_date - timedelta(days=7)
    today = end_date.date()
    yesterday = today - timedelta(days=1)
    cat_count = Category.objects.all().count()
    pass_count = Passes.objects.all().count()

    data_count_last_seven_days = Passes.objects.filter(passcreated_at__date__range=(start_date, end_date.date())).count()
    #data_count_last_seven_days = Passes.objects.filter(passcreated_at__date__range=(start_date, end_date)).count()

    data_count_today = Passes.objects.filter(passcreated_at__date=today).count()
    data_count_yesterday = Passes.objects.filter(passcreated_at__date=yesterday).count()

    return render(request, 'dashboard.html', {
        'data_count_last_seven_days': data_count_last_seven_days,
        'data_count_today': data_count_today,
        'data_count_yesterday': data_count_yesterday,
        'cat_count': cat_count,
        'pass_count': pass_count,
    })


login_required(login_url='/')


def PROFILE(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {
        "user": user,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name

            customuser.save()
            messages.success(request, "Your profile has been updated successfully")
            return redirect('profile')

        except:
            messages.error(request, "Your profile updation has been failed")
    return render(request, 'profile.html')


def CHANGE_PASSWORD(request):
    context = {}
    ch = User.objects.filter(id=request.user.id)
    if len(ch) > 0:
        data = User.objects.get(id=request.user.id)
        context["data"]: data
    if request.method == "POST":
        current = request.POST["cpwd"]
        new_pas = request.POST['npwd']
        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
            user.set_password(new_pas)
            user.save()
            messages.success(request, 'Password Change  Succeesfully!!!')
            user = User.objects.get(username=un)
            login(request, user)
        else:
            messages.success(request, 'Current Password wrong!!!')
            return redirect("change_password")
    return render(request, 'change-password.html')


@login_required(login_url='/')
def ADD_CATEGORY(request):
    if request.method == "POST":
        category_name = request.POST.get('categoryname')
        category = Category(
            categoryname=category_name,
        )
        category.save()
        messages.success(request, 'Category Added Succeesfully!!!')
        return redirect("add_category")

    return render(request, 'add_category.html')


@login_required(login_url='/')
def MANAGE_CATEGORY(request):
    category = Category.objects.all()
    context = {'category': category,

               }
    return render(request, 'manage_category.html', context)


def DELETE_Category(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    messages.success(request, 'Record Delete Succeesfully!!!')

    return redirect('manage_category')


login_required(login_url='/')


def UPDATE_Category(request, id):
    category = Category.objects.get(id=id)

    context = {
        'category': category,
    }

    return render(request, 'update-category.html', context)


def UPDATE_CATEGORY_DETAILS(request):
    if request.method == 'POST':
        cat_id = request.POST.get('cat_id')
        categoryname = request.POST['categoryname']
        category = Category.objects.get(id=cat_id)
        category.categoryname = categoryname
        category.save()
        messages.success(request, "Your category detail has been updated successfully")
        return redirect('manage_category')
    return render(request, 'update-category.html')





# utils/pdf_generator.py

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
import boto3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile


from pass_pdf_lib import generate_pass_pdf


# utils/s3_upload.py
import boto3
from botocore.exceptions import ClientError

def upload_pdf_to_s3(pdf_path, pass_number):
    s3 = boto3.client('s3')
    BUCKET_NAME = "s3-cpp-x23423625"
    s3_key = f"pass_{pass_number}"

    # ACL REMOVED → Required for buckets with ACLs disabled.
    s3.upload_file(pdf_path, BUCKET_NAME, s3_key)

    # Create presigned URL
    download_url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': BUCKET_NAME, 'Key': s3_key},
        ExpiresIn=3600  # 1 hour
    )
    return download_url



@login_required(login_url='/')
def ADD_PASSSES(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        pass_number = random.randint(100000000, 999999999)
        gender = request.POST.get('gender')
        profile_pic1 = request.FILES.get('profile_pic1')
        cnumber = request.POST.get('cnumber')
        email = request.POST.get('email')
        identitytype = request.POST.get('identitytype')
        icnum = request.POST.get('icnum')

        category_id = request.POST.get('category_id')
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        cost = request.POST.get('cost')

        categoryid = Category.objects.get(id=category_id)
        userpassdetail = Passes(fullname=fullname,
                                passnumber=pass_number,
                                gender=gender,
                                profile_pic1=profile_pic1,
                                mobilenumber=cnumber,

                                email=email,
                                identitytype=identitytype,
                                identitycardnumber=icnum,
                                category_id=categoryid,
                                source=source,
                                destinations=destination,
                                fromdate=fromdate,
                                todate=todate,
                                cost=cost
                                )

        userpassdetail.save()
        
        #Pypi 
        
         # ========== 1. GENERATE PDF ==========
        pdf_path = generate_pass_pdf(userpassdetail)
        pdf_filename = f"pass_{pass_number}.pdf"

        # ========== 2. UPLOAD PDF TO S3 ==========
        pdf_url = upload_pdf_to_s3(pdf_path, pdf_filename)

        # Delete local temp file
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

        # ========== 3. SEND EMAIL WITH PDF LINK ==========
        if pdf_url:
            msg = f"Your pass number: {pass_number}\nDownload your Pass PDF:\n{pdf_url}"
        else:
            msg = f"Your pass number: {pass_number}\nPDF could not be generated."
            
        print("===========>  PDF LINK : ",msg)

        send_email_api("Your Bus Pass", msg, email)

        
        
        #msg = f"Your pass number : {userpassdetail.passnumber}"
        #send_email_api("Pass generated",msg,userpassdetail.email)
        if s3_bucket_upload_img(profile_pic1, profile_pic1.name):
            print("FILE UPLOADED TO S3")
            #sns_msg = f"Pass generated successfully. Pass Number : {pass_number}"
            sns_msg = f"Pass No. {pass_number} \n Mode of transport : {userpassdetail.category_id.categoryname} \n Source : {source} \n Destination : {destination}" 
            if sns_email_send("Pass Generated",sns_msg):
                
                print("----------------->SNS MAIL SENT")
            else:
                print("----------------->SNS MAIL NOT SENT")
                
        else:print("FILE UPLOAD FAILED ...")

        msg = f"Bus Pass Created {pass_number}"
        messages.success(request, msg)
        return redirect('add_passes')
    category = Category.objects.all()
    context = {
        'category': category,
    }
    return render(request, 'add-passes.html', context)


@login_required(login_url='/')
def MANAGE_PASSES(request):
    userpasses = Passes.objects.all()
    paginator = Paginator(userpasses, 10)
    page = request.GET.get('page')
    userpasses = paginator.get_page(page)
    return render(request, 'manage_passes.html', {'userpasses': userpasses})


@login_required(login_url='/')
def my_view(request):
    items_list = Passes.objects.all()
    paginator = Paginator(items_list, 10)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    return render(request, 'myview.html', {'items': items})


@login_required(login_url='/')
def WEBSITE_UPDATE(request):
    page = Page.objects.all()
    context = {"page": page,

               }
    return render(request, 'website.html', context)


@login_required(login_url='/')
def UPDATE_WEBSITE_DETAILS(request):
    if request.method == 'POST':
        web_id = request.POST.get('web_id')
        pagetitle = request.POST['pagetitle']
        address = request.POST['address']
        aboutus = request.POST['aboutus']
        email = request.POST['email']
        mobilenumber = request.POST['mobilenumber']
        page = Page.objects.get(id=web_id)
        page.pagetitle = pagetitle
        page.address = address
        page.aboutus = aboutus
        page.email = email
        page.mobilenumber = mobilenumber
        page.save()
        messages.success(request, "Your website detail has been updated successfully")
        return redirect('website_update')
    return render(request, 'website.html')


def DELETE_PASSES(request, id):
    passes = Passes.objects.get(id=id)
    passes.delete()
    messages.success(request, 'Record Delete Succeesfully!!!')
    return redirect('manage_passes')


login_required(login_url='/')


def UPDATE_PASSES(request, id):
    passes = Passes.objects.get(id=id)
    context = {
        "passes": passes,
    }
    return render(request, 'update-passes.html', context)


login_required(login_url='/')


def VIEW_PASSES(request, id):
    passes = Passes.objects.get(id=id)

    context = {
        'passes': passes,
    }

    return render(request, 'view-passes.html', context)


def Search_Passes(request):
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            userpasses = Passes.objects.filter(passnumber__icontains=query)
            messages.success(request, "Search against " + query)
            return render(request, 'search-passes.html', {'userpasses': userpasses})
        else:

            print("No Record Found")
            return render(request, 'search-passes.html', {})


def data_between_dates(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        userpasses = Passes.objects.filter(passcreated_at__range=(start_date, end_date))
    else:
        userpasses = []

    return render(request, 'data_between_dates.html', {'userpasses': userpasses})
