from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from app import models 
from app.models import *
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from random import randrange
import datetime
from app.form import Userimage, Userimage2
from django.contrib.auth.decorators import login_required 
import csv
import requests
from django.conf import settings
from django.http import JsonResponse
import csv
from django.contrib.admin.views.decorators import staff_member_required
from django.apps import apps

@staff_member_required
def global_search_export(request):
    models = apps.get_models()
    search_query = request.GET.get('q', '')
    results = []

    if search_query:
        for model in models:
            model_name = model._meta.verbose_name_plural
            try:
                fields = [
                    field for field in model._meta.get_fields()
                    if hasattr(field, "get_internal_type") and field.get_internal_type() in ["CharField", "TextField"]
                ]
                queryset = model.objects.filter(
                    **{f"{field.name}__icontains": search_query for field in fields}
                )
                if queryset.exists():
                    results.append((model_name, queryset))
            except Exception as e:
                # Log or print error for debugging
                print(f"Error processing model {model_name}: {e}")
                continue


    # Export to CSV if requested
    if 'export' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="global_search_results.csv"'
        writer = csv.writer(response)

        writer.writerow(['Model', 'ID', 'Data'])  # Header
        for model_name, queryset in results:
            for obj in queryset:
                writer.writerow([model_name, obj.id, str(obj)])

        return response

    return render(request, 'admin/global_search.html', {'results': results, 'search_query': search_query})

def search_and_export(request):
    students = None
    if request.method == 'POST':
        name = request.POST.get('name', '')
        session = request.POST.get('session', '')
        department = request.POST.get('department', '')
        regNo = request.POST.get('regNo', '')

        # Filter students based on search criteria
        students = AddStudents.objects.all()
        if name:
            students = students.filter(name__icontains=name)
        if session:
            students = students.filter(session=session)
        if department:
            students = students.filter(department=department)
        if regNo:
            students = students.filter(regNo=regNo)

        # Handle Excel export
        if 'export' in request.POST:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="students.csv"'
            writer = csv.writer(response)
            writer.writerow(['Name', 'Session', 'department', 'regNo'])  # Header
            for student in students:
                writer.writerow([student.name, student.session, student.department, student.regNo])
            return response

    return render(request, 'admin/search_export.html', {'students': students})

def verify_payment(request, reference):
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    if data['status'] and data['data']['status'] == 'success':
        # Payment successful
        return render(request, 'payment_success.html', {'data': data['data']})
    else:
        # Payment failed
        return render(request, 'payment_failed.html', {'error': data['message']})

# Create your views here.
def home(request):
    info = news.objects.all()
    one_info = info[2]
    return render(request,'home.html', {'one_info': one_info})
def allNews(request):
    info = news.objects.all()
    one_info = info[0]
    print(info)
    return render(request,'news.html', {'info': info})
def application(request):
    img =Userimage(request.POST, request.FILES)
    if request.method == 'POST':
        if img.is_valid():
            token =request.POST['token']
            name = request.POST['yourname']
            email = request.POST['email']
            address = request.POST['address']
            phone = request.POST['phone']
            gender= request.POST['gender']
            marital = request.POST['marital']
            dateOfBirth = request.POST['dob']
            courseName = request.POST['courses']
            primaryName = request.POST['primary']
            pcompletionYear = request.POST['pcopletionyear']
            secondaryName = request.POST['secondary']
            scompletionYear = request.POST['scopletionyear']
            examType = request.POST['etype']
            examYear = request.POST['eyear']
            english = request.POST['english']
            mathematics = request.POST['mathematics']
            biology = request.POST['biology']
            chemistry = request.POST['chemistry']
            physics = request.POST['physics']
            form =Applications(token=token, email=email, name=name, address=address, phone=phone, gender=gender, marital=marital,
            dateOfBirth=dateOfBirth, courseName=courseName, primaryName=primaryName, pcompletionYear=pcompletionYear,secondaryName=secondaryName,
            scompletionYear=scompletionYear, examType=examType, examYear=examYear,english=english,mathematics=mathematics,
            biology=biology, chemistry=chemistry, physics=physics)
            pic = request.FILES.get('passport')
            form.passport=pic
            form.save()
            prefix =Customize.objects.order_by('id').values_list('app_id_prefix', flat=True).last()
            #print(prefix)
            return render(request, 'Examslip.html', {'form': form, 'prefix':prefix})
        else:
            img =Userimage()
            return render(request, 'Admission_page.html', {'img': img})
    return render(request, 'Admission_page.html', {'img': img})
def contact(request):
    return render(request, 'Contact_page.html')
def submitcontact(request):
    if request.method =="POST":
        cname = request.POST['cname']
        cemail = request.POST['cemail']
        cmessage = request.POST['cmessage']
        form =Contact(cname=cname, cemail=cemail, cmessage=cmessage)
        form.save()
    return render(request, 'Contact_page.html')
def register(request):
    if request.method =="POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['psw']
        cpassword = request.POST['confirm']
        if password == cpassword:
            user_check = User.objects.filter(username=username)
            if len(user_check) > 0:
                err='User already exist try login'
                uploadedregno = AddStudents.objects.values_list('regNo')
                return render(request, 'index.html', {'uploadedregno': uploadedregno, 'err':err})
            else:
                user =User.objects.create_user(username=username, email=email, password=password)
                user.save()
                std =Students(regNo=username, email=email)
                std.save()
                success = 'Registration Successfull !!!, Login to Continue'
                return render(request, 'index.html',{'success':success})
        
        else:
            err='password not martch..'
            uploadedregno = AddStudents.objects.values_list('regNo')
            return render(request, 'index.html', {'uploadedregno': uploadedregno, 'err':err})
def login_func(request):
    if request.method =="POST":
        username = request.POST['uname']
        password = request.POST['lpsw']

        user =authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            user_program = AddStudents.objects.filter(regNo=username).values()
            #find_id =Ict.objects.get(regNo=username).id
            user_info = Students.objects.filter(regNo=username).values()
            request.session['username'] = username
            print(user_info)
            return redirect('student')
        else:
            errr ='incorrect username or password !!!'
            return render(request,'index.html',{'errr': errr})
    else:
        uploadedregno = AddStudents.objects.values_list('regNo')
        uploadedregno = list(uploadedregno)
        return render(request, 'index.html', {'uploadedregno': uploadedregno })
@login_required(login_url='/login_func/')
def student(request):
    username=request.session.get('username', 'Guest')
    if request.user.is_authenticated:
        print(username)
        user_program = AddStudents.objects.filter(regNo=username).values()
        user_info = Students.objects.filter(regNo=username).values()
        img = get_object_or_404(Students, regNo=username)
        return render(request, 'profile.html', {'user_program': user_program, 'user_info': user_info, 'img':img})
    else:
        return render(request, 'index.html')
def token(request):
    userlog = TokenUser.objects.all()
    if request.method =="POST":
        return render(request, 'profile2.html')
    else:
        return render(request, 'profile2.html', {'userlog':userlog})
def gentoken(request):
    if request.method =="POST":
        tokenNo = request.POST['tokenNo']
        dt =request.POST['dt']
        for i in range(int(tokenNo)):
            num = randrange(1000000000,99999999999)
            savetoken = GenToken(tokenNo=num, date=dt)
            #savetoken.save()
        reToken=GenToken.objects.all()
        return render(request, 'gentoken.html', {'reToken': reToken})
    else:
        return render(request, 'gentoken.html')
def profile(request):
    if request.method =="POST":
        regNo = request.POST['regNo']
        email = request.POST['email']
        address =request.POST['address']
        phone = request.POST['phone']
        gender= request.POST['gender']
        marital = request.POST['marital_status']
        dateOfBirth =request.POST['dateob']
        status = request.POST['std_custome6']
        adm_reference = request.POST['admin_reference']
        nationality = request.POST['nationality']
        home_town = request.POST['home']
        place_of_birth = request.POST['place']
        state = request.POST['state']
        lga =request.POST['lga']
        program_type =request.POST['programme']
        n_name=request.POST['n_name']
        n_address=request.POST['n_address']
        n_phone=request.POST['n_phone']
        n_email=request.POST['n_email']
        n_relationship=request.POST['n_relationship']
        disability=request.POST['disability']
        blood_grp=request.POST['blood_grp']
        genotype=request.POST['genotype']
        sponsor=request.POST['sponsor']
        sponsor_name=request.POST['sponsor_name']
        sport=request.POST['sport']
        extra_activities=request.POST['extra_activities']

        std =Students(regNo=regNo, extra_activities=extra_activities,sport=sport,sponsor_name=sponsor_name, email=email,sponsor=sponsor,
        genotype=genotype,blood_grp=blood_grp,disability=disability,n_relationship=n_relationship,n_email=n_email,n_phone=n_phone,
        n_address=n_address,n_name=n_name, program_type=program_type,lga=lga, state=state,place_of_birth=place_of_birth,home_town=home_town,
        nationality=nationality,adm_reference=adm_reference,status=status,dateOfBirth=dateOfBirth,marital=marital,
        gender=gender,phone=phone,address=address)
        img =Userimage2(request.POST, request.FILES)
        pic = request.FILES.get('passport')
        std.passport=pic
        std.save()
        return redirect( 'student')
def exam_slip(request):
    if request.method == 'POST':
        appNo = request.POST['pemail']
        form=''
        img =''
        prefix =Customize.objects.order_by('id').values_list('app_id_prefix', flat=True).last()
        if appNo.find('@') != -1:
            form = Applications.objects.filter(email=appNo).values()
            img = get_object_or_404(Applications, email=appNo)
        else:
            rprefix=appNo.replace(str(prefix),'')
            form = Applications.objects.filter(id=rprefix).values()
            img = get_object_or_404(Applications, id=rprefix)
        form = form[0]
        form['id']=prefix + form['id']
        #exam_info= Application.objects.
        print(form['passport'])
        return render(request, 'Examslip.html', {'form': form, 'img':img})
    return render(request, 'admission_page.html')

def test(request):
    return render(request, 'paystack.html')
def result(request):
     if request.user.is_authenticated:
        username=request.session.get('username', 'Guest')
        user_program = AddStudents.objects.filter(regNo=username).values()
        user_info = Students.objects.filter(regNo=username).values()
        find_id =AddStudents.objects.get(regNo=username).regNo
        img = get_object_or_404(Students, regNo=username)
        return render(request, 'result.html', {'user_program': user_program, 'user_info': user_info, 'img':img})
def payment(request):
    if request.user.is_authenticated:
        username=request.session.get('username', 'Guest')
        user_program = AddStudents.objects.filter(regNo=username).values()
        user_info = Students.objects.filter(regNo=username).values()
        find_id =AddStudents.objects.get(regNo=username).regNo
        payment_info = Payments.objects.filter(students_id=find_id).values()
        img = get_object_or_404(Students, regNo=username)
        return render(request, 'paymenthistory.html', {'payment_info': payment_info, 'user_program': user_program, 'user_info': user_info, 'img':img})
def examcard(request):
     if request.user.is_authenticated:
        username=request.session.get('username', 'Guest')
        user_program = AddStudents.objects.filter(regNo=username).values()
        user_info = Students.objects.filter(regNo=username).values()
        find_id =AddStudents.objects.get(regNo=username).regNo
        payment_info = Payments.objects.filter(students_id=find_id).values()
        img = get_object_or_404(Students, regNo=username)
        return render(request, 'examcard.html', {'payment_info': payment_info, 'user_program': user_program, 'user_info': user_info, 'img':img})
def course(request):
     if request.user.is_authenticated:
        username=request.session.get('username', 'Guest')
        user_program = AddStudents.objects.filter(regNo=username).values()
        user_info = Students.objects.filter(regNo=username).values()
        find_id =AddStudents.objects.get(regNo=username).regNo
        img = get_object_or_404(Students, regNo=username)
        print(user_info)
        return render(request, 'coursehistory.html', { 'user_program': user_program, 'user_info': user_info, 'img':img})
def getSemester(request):
    if request.user.is_authenticated:
        get_id = request.GET.get('id')
        lv= get_id.split('_')
        level =int(lv[0])
        semester = lv[1]
        username=request.session.get('username', 'Guest')
        user_program = AddStudents.objects.filter(regNo=username).values()
        user_info = Students.objects.filter(regNo=username).values()
        try:
            find_user =CourseRegistration.objects.get(students_id=username)
            department =AddStudents.objects.get(regNo=username).department
            
            print(department)
            reg_courses = Courses.objects.filter(semester=semester, level=level, program=department.upper()).values()
            img = get_object_or_404(Students, regNo=username)
            if len(reg_courses) > 0:
                return render(request, 'course.html', { 'level':level, 'semester':semester, 'user_program': user_program, 'reg_courses': reg_courses, 'user_info': user_info, 'img':img})
            else:
                return HttpResponse('no courses registration')
        except CourseRegistration.DoesNotExist:
            return HttpResponse('no course registration !!!')
def getExamCard(request):
    if request.user.is_authenticated:
        get_id = request.GET.get('id')
        lv= get_id.split('_')
        level =int(lv[0])
        semester = lv[1]
        username=request.session.get('username', 'Guest')
        user_program = AddStudents.objects.filter(regNo=username).values()
        user_info = Students.objects.filter(regNo=username).values()
        find_id =AddStudents.objects.get(regNo=username).regNo
        reg_courses = Courses.objects.filter(semester=semester, level=level).values()
        img = get_object_or_404(Students, regNo=username)
        if len(reg_courses) > 0:
            return render(request, 'ecard.html', { 'level':level, 'semester':semester, 'user_program': user_program, 'reg_courses': reg_courses, 'user_info': user_info, 'img':img})
        else:
             return HttpResponse('no course registration')

