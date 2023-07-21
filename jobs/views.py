from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import date
import time
from django.core.mail import send_mail
from django.conf import settings
from .forms import *

def activity(action,time,actor):
    Activity.objects.create(action=action,time=time,actor=actor)

def index(request):
    return render(request, "index.html")

def user_login(request):
    if request.user.is_authenticated:
        return redirect("/user_homepage")
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            try:
                account = authenticate(username=User.objects.get(email=username).username,password=password)
                if account is not None:
                    login(request, account)
                    try:
                        utype = Applicant.objects.get(user=User.objects.get(email=username))
                        if utype is not None:
                            return redirect('/all_jobs')
                    except:
                        try:
                            ctype = Company.objects.get(user=User.objects.get(email=username))
                            if ctype is not None:
                                return redirect('/company_homepage')
                        except:
                            return redirect('/all_companies')
                else:
                    messages.warning(request,"Invalid Credentials")
            except:
                account = authenticate(username=username, password=password)
                if account is not None:
                    login(request, account)
                    try:
                        utype = Applicant.objects.get(user=User.objects.get(username=username))
                        if utype is not None:
                            return redirect('/all_jobs')
                    except:
                        try:
                            ctype = Company.objects.get(user=User.objects.get(username=username))
                            if ctype is not None:
                                return redirect('/company_homepage')
                        except:
                            return redirect('/all_companies')
                else:
                    messages.warning(request,"Invalid Credentials")
    return render(request, "user_login.html")

def edituser(request):
    if not request.user.is_authenticated:
        return redirect('/user_login/')
    applicant = Applicant.objects.get(user=request.user)
    if request.method=="POST":   
        email = request.POST.get('email')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')

        applicant.user.email = email
        applicant.user.first_name = first_name
        applicant.user.last_name = last_name
        applicant.phone = phone
        applicant.gender = gender
        applicant.save()
        applicant.user.save()

        try:
            image = request.FILES['image']
            applicant.image = image
            applicant.save()
        except:
            pass
        showtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        activity("Edited profile",showtime,request.user)
        messages.success(request,"Profile Updated")
        return redirect("/user_homepage/")
    return render(request, "edituser.html", {'applicant':applicant})

def edit_pass(request):
    user = request.user
    if not request.user.is_authenticated:
        return redirect('/user_login/')
    try:
        applicant = Applicant.objects.get(user=request.user)
        if request.method=="POST":
            old_pass = request.POST.get('old_pass')
            new_pass1 = request.POST.get('new_pass1')
            new_pass2 = request.POST.get('new_pass2')
            account = authenticate(username=request.user,password=old_pass)
            if account is None:
                messages.warning(request,"Incorrect Password")
            else:
                if new_pass1 != new_pass2:
                    messages.warning(request,"Passwords do not match")
                else:
                    try:
                        applicant.user.set_password(new_pass1)
                        applicant.save()
                        applicant.user.save()
                    except:
                        messages.warning(request,"Something went wrong")
                    messages.success(request,"Password has been changed")
                    return redirect("/user_homepage")
    except:
        company = Company.objects.get(user=request.user)
        if request.method=="POST":
            old_pass = request.POST.get('old_pass')
            new_pass1 = request.POST.get('new_pass1')
            new_pass2 = request.POST.get('new_pass2')
            account = authenticate(username=request.user,password=old_pass)
            if account is None:
                messages.warning(request,"Incorrect Password")
            else:
                if new_pass1 != new_pass2:
                    messages.warning(request,"Passwords do not match")
                else:
                    try:
                        company.user.set_password(new_pass1)
                        company.save()
                        company.user.save()
                    except:
                        messages.warning(request,"Something went wrong")
                    messages.success(request,"Password has been changed")
                    return redirect("/company_homepage")
    return render(request,"edit_pass.html",{'user':user})

def user_homepage(request):
    if not request.user.is_authenticated:
        return redirect('/user_login/')
    applicant = Applicant.objects.get(user=request.user)
    return render(request, "user_homepage.html", {'applicant':applicant})

def all_jobs(request):
    jobs = Job.objects.filter(status="Accepted").order_by('-start_date')
    applicant = Applicant.objects.get(user=request.user)
    apply = Application.objects.filter(applicant=applicant)
    data = []
    for i in apply:
        data.append(i.job.id)
    return render(request, "all_jobs.html", {'jobs':jobs, 'data':data})

def job_detail(request, myid):
    job = Job.objects.get(id=myid)
    return render(request, "job_detail.html", {'job':job})

def job_apply(request, myid):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    applicant = Applicant.objects.get(user=request.user)
    job = Job.objects.get(id=myid)
    date1 = date.today()
    if job.end_date < date1:
        messages.warning(request,"Job is already close")
        return render(request, "job_apply.html")
    elif job.start_date > date1:
        messages.warning(request,"Job is not yet open")
        return render(request, "job_apply.html")
    else:
        if request.method == "POST":
            resume = request.FILES['resume']
            Application.objects.create(job=job, company=job.company, applicant=applicant, resume=resume, apply_date=date.today())
            showtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            activity("Applied for a job",showtime,request.user)
            messages.success(request,"Application Sent")
            return redirect("/all_jobs")
    return render(request, "job_apply.html", {'job':job})

def all_applicants(request):
    company = Company.objects.get(user=request.user)
    application = Application.objects.filter(company=company)
    return render(request, "all_applicants.html", {'application':application})

def signup(request):
    if request.method=="POST":   
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        image = request.FILES.get('image')

        if User.objects.filter(username = username).first():
            messages.warning(request, "This username is already taken")
            return redirect('/signup')
        if User.objects.filter(email = email).first():
            messages.warning(request, "This email is already taken")
            return redirect('/signup')
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/signup')
        
        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password1)
        applicants = Applicant.objects.create(user=user, phone=phone, gender=gender, image=image, type="applicant")
        try:
            user.save()
            applicants.save()
        except:
            messages.warning(request,"Something Went wrong")
        messages.success(request,"Account Created Successfully")
        return redirect("/user_login")
    return render(request, "signup.html")

def company_changepass(request):
    user = request.user
    if not request.user.is_authenticated:
        return redirect('/user_login/')
    try:
        applicant = Applicant.objects.get(user=request.user)
        if request.method=="POST":
            old_pass = request.POST.get('old_pass')
            new_pass1 = request.POST.get('new_pass1')
            new_pass2 = request.POST.get('new_pass2')
            account = authenticate(username=request.user,password=old_pass)
            if account is None:
                messages.warning(request,"Incorrect Password")
            else:
                if new_pass1 != new_pass2:
                    messages.warning(request,"Passwords do not match")
                else:
                    try:
                        applicant.user.set_password(new_pass1)
                        applicant.save()
                        applicant.user.save()
                    except:
                        messages.warning(request,"Something went wrong")
                    messages.success(request,"Password has been changed")
                    return redirect("/user_homepage")
    except:
        company = Company.objects.get(user=request.user)
        if request.method=="POST":
            old_pass = request.POST.get('old_pass')
            new_pass1 = request.POST.get('new_pass1')
            new_pass2 = request.POST.get('new_pass2')
            account = authenticate(username=request.user,password=old_pass)
            if account is None:
                messages.warning(request,"Incorrect Password")
            else:
                if new_pass1 != new_pass2:
                    messages.warning(request,"Passwords do not match")
                else:
                    try:
                        company.user.set_password(new_pass1)
                        company.save()
                        company.user.save()
                    except:
                        messages.warning(request,"Something went wrong")
                    messages.success(request,"Password has been changed")
                    return redirect("/company_homepage")
    return render(request,"company_changepass.html",{'user':user})

def company_signup(request):
    if request.method=="POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        image = request.FILES.get('image')
        company_name = request.POST.get('company_name')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/company_signup')
        try:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password1)
            company = Company.objects.create(user=user, phone=phone, gender=gender, image=image, company_name=company_name, type="company", status="pending")
            user.save()
        except:
            return redirect("/company_signup")
        try:
            company.save()
        except:
            return redirect("/user_login")
        return redirect("/user_login")
    
    return render(request, "company_signup.html")

def company_homepage(request):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    company = Company.objects.get(user=request.user)
    return render(request, "company_homepage.html", {'company':company})

def edit_company(request):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    company = Company.objects.get(user=request.user)
    if request.method=="POST":   
        email = request.POST.get('email')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')

        company.user.email = email
        company.user.first_name = first_name
        company.user.last_name = last_name
        company.phone = phone
        company.gender = gender
        company.save()
        company.user.save()

        try:
            image = request.FILES['image']
            company.image = image
            company.save()
        except:
            pass
        showtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        activity("Edited profile",showtime,request.user)
        messages.success(request,"Profile updated successfully")
        return redirect("/company_homepage")
    return render(request,"editcompany.html",{'company':company})

def add_job(request):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    if request.method == "POST":
        title = request.POST.get('job_title')
        city = request.POST.get('city')
        country = request.POST.get('country')
        job_class = request.POST.get('job_class')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        salary = request.POST.get('salary')
        experience = request.POST.get('experience')
        skills = request.POST.get('skills')
        description = request.POST.get('description')
        user = request.user
        company = Company.objects.get(user=user)
        applicants = Applicant.objects.all()
        recipients = []
        for a in applicants:
            recipients.append(a.user.email)

        job = Job.objects.create(company=company, title=title, city=city,country=country, job_type=job_class, status="Pending", start_date=start_date, end_date=end_date, salary=salary, image=company.image, experience=experience, skills=skills, description=description, creation_date=date.today())
        job.save()
        send_mail('New Job listing at Job Avenue','A new '+title+" job was posted!", 'raymartarceona@gmail.com',recipients)
        showtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        activity("Posted a job",showtime,request.user)
        messages.success(request,"Job now waiting for approval")
        return redirect("/job_list")
    return render(request, "add_job.html")

def job_list(request):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    companies = Company.objects.get(user=request.user)
    jobs = Job.objects.filter(company=companies)
    return render(request, "job_list.html", {'jobs':jobs})

def edit_job(request, myid):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    job = Job.objects.get(id=myid)
    if request.method == "POST":
        title = request.POST.get('job_title')
        job_class = request.POST.get('job_class')
        status = request.POST.get('status')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        salary = request.POST.get('salary')
        experience = request.POST.get('experience')
        city = request.POST.get('city')
        country = request.POST.get('country')
        skills = request.POST.get('skills')
        description = request.POST.get('description')

        job.title = title
        job.job_type = job_class
        job.salary = salary
        job.experience = experience
        job.city = city
        job.country = country
        job.skills = skills
        job.status = status
        job.description = description

        job.save()
        if start_date:
            job.start_date = start_date
            job.save()
        if end_date:
            job.end_date = end_date
            job.save()
        showtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        activity("Edited a job",showtime,request.user)
        messages.success(request,"Job details updated successfully")
        return redirect("/job_list")
    return render(request, "edit_job.html", {'job':job})

def delete_job(request,myid):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    job = Job.objects.filter(id=myid)
    job.delete()
    showtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    activity("Deleted a job",showtime,request.user)
    return redirect("/job_list")

def company_logo(request, myid):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    job = Job.objects.get(id=myid)
    if request.method == "POST":
        image = request.FILES['logo']
        job.image = image 
        job.save()
        messages.success(request,"Company logo updated successfully.")
        return redirect("/company_logo")
    return render(request, "company_logo.html", {'job':job})

def Logout(request):
    logout(request)
    return redirect('/')

def view_applicants(request):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    applicants = Applicant.objects.all()
    return render(request, "view_applicants.html", {'applicants':applicants})

def edit_applicant(request,aid):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    user = User.objects.get(id=aid)
    applicant = Applicant.objects.get(user=user)

    if request.method == "POST":
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        uname = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')

        applicant.user.first_name = fname
        applicant.user.last_name = lname
        applicant.user.username = uname
        applicant.user.email = email
        applicant.gender = gender
        applicant.phone = phone
        applicant.save()
        applicant.user.save()
        messages.success(request,"Success.")
        return redirect("/view_applicants")
    return render(request,"edit_applicant.html",{'applicant':applicant})

def delete_applicant(request, aid):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    applicant = User.objects.filter(id=aid)
    applicant.delete()
    return redirect("/view_applicants")

def applicant_info(request,aid):
    user = User.objects.get(id=aid)
    applicant = Applicant.objects.get(user=user)
    applications = Application.objects.filter(applicant=applicant)

    return render (request,"applicant_info.html",{'user':user,'applicant':applicant,'applications':applications})

def pending_companies(request):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    companies = Company.objects.filter(status="Pending")
    return render(request, "pending_companies.html", {'companies':companies})

def change_status(request, myid):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    company = Company.objects.get(id=myid)

    if request.method == "POST":
        status = request.POST.get('status')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        uname = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')

        company.user.first_name = fname
        company.user.last_name = lname
        company.user.username = uname
        company.user.email = email
        company.gender = gender
        company.phone = phone
        company.status=status
        company.save()
        company.user.save()
        messages.success(request,"Success.")
        return redirect("/all_companies")
    return render(request, "change_status.html", {'company':company})

def accepted_companies(request):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    companies = Company.objects.filter(status="Accepted")
    return render(request, "accepted_companies.html", {'companies':companies})

def rejected_companies(request):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    companies = Company.objects.filter(status="Rejected")
    return render(request, "rejected_companies.html", {'companies':companies})

def all_companies(request):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    companies = Company.objects.all()
    return render(request, "all_companies.html", {'companies':companies})

def delete_company(request, myid):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    company = User.objects.filter(id=myid)
    company.delete()
    return redirect("/all_companies")

def listed_jobs(request):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    jobs = Job.objects.all()
    return render(request,"listed_jobs.html",{'jobs':jobs})

def accepted_jobs(request):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    jobs = Job.objects.filter(status="Accepted")
    return render(request,"accepted_jobs.html",{'jobs':jobs})

def rejected_jobs(request):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    jobs = Job.objects.filter(status="Rejected")
    return render(request,"rejected_jobs.html",{'jobs':jobs})

def pending_jobs(request):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    jobs = Job.objects.filter(status="Pending")
    return render(request,"pending_jobs.html",{'jobs':jobs})

def admin_editjob(request, myid):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    job = Job.objects.get(id=myid)
    if request.method == "POST":
        title = request.POST.get('job_title')
        status = request.POST.get('status')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        salary = request.POST.get('salary')
        experience = request.POST.get('experience')
        city = request.POST.get('city')
        country = request.POST.get('country')
        skills = request.POST.get('skills')
        description = request.POST.get('description')

        job.title = title
        job.status = status
        job.salary = salary
        job.experience = experience
        job.city = city
        job.country = country
        job.skills = skills
        job.description = description

        job.save()
        if start_date:
            job.start_date = start_date
            job.save()
        if end_date:
            job.end_date = end_date
            job.save()
        messages.success(request,"Job details updated successfully")
        return redirect("/listed_jobs")
    return render(request, "admin_editjob.html", {'job':job})

def admin_deletejob(request,myid):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    job = Job.objects.filter(id=myid)
    job.delete()
    return redirect("/listed_jobs")

def admin_editpass(request,uid):
    if not request.user.is_authenticated:
        return redirect('/user_login/')
    try:
        user = User.objects.get(id=uid)
        applicant = Applicant.objects.get(user=user)
        if request.method=="POST":
            old_pass = request.POST.get('old_pass')
            new_pass1 = request.POST.get('new_pass1')
            new_pass2 = request.POST.get('new_pass2')
            account = authenticate(username=request.user,password=old_pass)
            if account is None:
                messages.warning(request,"Incorrect Password")
            else:
                if new_pass1 != new_pass2:
                    messages.warning(request,"Passwords do not match")
                else:
                    try:
                        applicant.user.set_password(new_pass1)
                        applicant.save()
                        applicant.user.save()
                    except:
                        messages.warning(request,"Something went wrong")
                    messages.success(request,"Password has been changed")
                    return redirect("/view_applicants")
    except:
        company = Company.objects.get(user=user)
        if request.method=="POST":
            old_pass = request.POST.get('old_pass')
            new_pass1 = request.POST.get('new_pass1')
            new_pass2 = request.POST.get('new_pass2')
            account = authenticate(username=request.user,password=old_pass)
            if account is None:
                messages.warning(request,"Incorrect Password")
            else:
                if new_pass1 != new_pass2:
                    messages.warning(request,"Passwords do not match")
                else:
                    try:
                        company.user.set_password(new_pass1)
                        company.save()
                        company.user.save()
                    except:
                        messages.warning(request,"Something went wrong")
                    messages.success(request,"Password has been changed")
                    return redirect("/all_companies")
    return render(request,"admin_editpass.html")

def activity_logs(request):
    activities = Activity.objects.all()
    return render(request,"activity_logs.html",{'activities':activities})