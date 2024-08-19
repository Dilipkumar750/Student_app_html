from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib  import messages
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from .models import  score,CustomUser,Grant,Loan,incentive,job,study_meterial,video_meterial,category,subject_name,question_paper



def view_incentive(request):
    data = incentive.objects.all()
    return render(request,'view_incentive.html',{'data':data})

def view_load(request):
    data = Loan.objects.all()
    return render(request,'view_loan.html',{'data':data})

def view_grants(request):
    data = Grant.objects.all()
    return render(request,'view_grants.html',{'data':data})




def stu_more_information(request):
    return render(request,'stu_more_information.html')



def test(request, id):
    data = CustomUser.objects.get(username=request.user)
    sub_data = get_object_or_404(subject_name, sub=id)
    sub_values = question_paper.objects.filter(user=data.student_guid, test_id=sub_data.id)
    
    if request.method == 'POST':
        scoree = 0  
        ques = 0     
        
        for key, value in request.POST.items():
            if key.startswith('answer_'):
                if value == sub_values[ques].correct_answer:
                    scoree+=1                    
                ques+=1
        wrong = ques-scoree 
        try:
            score_data = score.objects.get(user = request.user)
            score_data.test_id = sub_data.sub             
            score_data.student_score = scoree
            score_data.worng_ans = wrong
            score_data.tot = ques
            score_data.save()            
        except:
            score.objects.create(user = request.user,tot = ques,worng_ans = wrong,test_id = sub_data.sub,student_score = scoree)
        return redirect('/progress')  # Redirect to a success page or another view

    return render(request, 'test.html', {'data': sub_values})



def choose_test(request):
    data = CustomUser.objects.get(username = request.user)
    sub_values = subject_name.objects.filter(user=data.student_guid).values('sub').distinct()
    score_data = score.objects.filter(user = request.user)
    return render(request,'choose_test.html',{'data':sub_values})

def progress(request):
    score_data = score.objects.filter(user = request.user)
    return render(request,'progress.html',{'score_data':score_data})

def add_questions(request,id):
    test_ids = question_paper.objects.filter(user=request.user, test_id=int(id)).values('test_id')
    data = question_paper.objects.filter(test_id__in=[item['test_id'] for item in test_ids])
    if request.method == 'POST':
        question = request.POST.get('question')
        obtionA = request.POST.get('obtionA')
        obtionB = request.POST.get('obtionB')
        obtionC = request.POST.get('obtionC')
        obtionD = request.POST.get('obtionD')
        correct_answer = request.POST.get('correct_answer')
        question_paper.objects.create(user = request.user,test_id = int(id),question = question,obtionA = obtionA,obtionB = obtionB,obtionC = obtionC,obtionD = obtionD,correct_answer = correct_answer)
    return render(request,'add_question.html',{'data':data})


def add_test(request):
    data = subject_name.objects.filter(user = request.user)
    if request.method == 'POST':
        categoryy = request.POST.get('sub')
        subject_name.objects.create(user = request.user,sub=categoryy)
        return redirect('/add_test')
    return render(request,'add_test.html',{'data':data})

def books(request):
    data = CustomUser.objects.get(username = request.user)
    meterial = study_meterial.objects.filter(user = data.student_guid)
    return render(request,'books.html',{'meterial':meterial})

def videos(request):
    data = CustomUser.objects.get(username = request.user)
    video = video_meterial.objects.filter(user = data.student_guid)
    return render(request,'vidoe.html',{'video':video})



def study_material(request):
    return render(request,'study_material.html')


def delete_video_met(request, id):
    data = video_meterial.objects.get(id=id)
    data.video.delete()
    data.delete()  
    return redirect('/add_video_material')



def delete_material(request, id):
    data = study_meterial.objects.get(id=id)
    data.meterial.delete()
    data.delete()  
    return redirect('/add_study_material')


def del_category(request, id):
    data = category.objects.get(id=id)
    data.delete()  
    return redirect('/add_category')

def add_category(request):
    data = category.objects.filter(user = request.user)
    if request.method == 'POST':
        categoryy = request.POST.get('category')
        category.objects.create(user = request.user,categoryy=categoryy)
        return redirect('/add_category')
    return render(request,'add_category.html',{'data':data})


def add_video_material(requset):
    data = category.objects.all()
    material_data = video_meterial.objects.filter(user = requset.user)
    if requset.method == 'POST':
        categoryy = requset.POST.get('category')
        file = requset.FILES.get('file')
        video_meterial.objects.create(user = requset.user,category = categoryy,video=file)
        return redirect('/add_video_material')
    return render(requset,'add_video_material.html',{'data':data,'material_data':material_data})

def add_study_material(requset):
    data = category.objects.all()
    material_data = study_meterial.objects.filter(user = requset.user)
    if requset.method == 'POST':
        categoryy = requset.POST.get('category')
        file = requset.FILES.get('file')
        study_meterial.objects.create(user = requset.user,category = categoryy,meterial=file)
        return redirect('/add_study_material')
    return render(requset,'add_study_material.html',{'data':data,'material_data':material_data})
 
def payment(request,id):
    data =  CustomUser.objects.get(username = request.user)
    if data.payment == 'success':
        return redirect('/mentor_access')
    else:
        fac_data =  CustomUser.objects.get(id = id)
        if request.method == 'POST':
            user_data = CustomUser.objects.get(username = request.user)
            user_data.student_guid = int(id)
            user_data.student_conformation = 'waiting'
            user_data.payment == 'success'
            user_data.save()
            return redirect('/mentor_access')
        return render(request,'payment.html',{'fac_data':fac_data})

def view_student_details(request,id):
    data = CustomUser.objects.get(id = id)
    if request.method == 'POST':
        print(data.student_conformation)
        subject = 'course code'
        message = 'your code is: '+data.contact+''
        from_email = 'abishek14052018@gmail.com'
        recipient_list = [data.email]
        email = EmailMessage(subject, message, from_email, recipient_list)
        email.send()
        data.student_conformation = 'success'
        data.save()
        return redirect('/Student_request')
    return render(request,'view_student_detail.html',{'data':data})



def Student_request(request):
    data = CustomUser.objects.get(username = request.user)
    student_data = CustomUser.objects.filter(student_guid = data.id,student_conformation = 'waiting')
    return render(request,'Student_request.html',{'data':student_data})

def mentor_access(request):
    data = CustomUser.objects.filter(user_type = 2)
    user_det = get_object_or_404(CustomUser, username=request.user)
    try:
        user_guid = CustomUser.objects.get(id = user_det.student_guid)
    except:
        user_guid = 'None'
    return render(request,'mentor_access.html',{'data':data,'user_det':user_det,'user_guid':user_guid})

def faq(request):
    return render(request,'faq.html')

def privacy_and_policy(request):
    return render(request,'privacy_and_policy.html')


def terms_and_conditions(request):
    return render(request,'terms_and_conditions.html')

def add_job(request):
    data = job.objects.all()
    if request.method == 'POST':
        img = request.FILES.get('img')
        title = request.POST.get('titile')
        point = request.POST.get('point')
        job.objects.create(img = img,title=title, point=point)
        return redirect('/add_job')
    return render(request,'add_job.html',{'data':data})

def job_delet(request,id):
    data = job.objects.get(id = id)
    data.img.delete()
    data.delete()
    return redirect('/add_job')






def add_incentive(request):
    data = incentive.objects.all()
    if request.method == 'POST':
        title = request.POST.get('titile')
        point = request.POST.get('point')
        incentive.objects.create(title=title, point=point)
        return redirect('/add_incentive')
    return render(request,'add_incentive.html',{'data':data})
def incentive_delet(request,id):
    data = incentive.objects.get(id = id)
    data.delete()
    return redirect('/add_incentive')


def add_loans(request):
    data = Loan.objects.all()
    if request.method == 'POST':
        title = request.POST.get('titile')
        point = request.POST.get('point')
        Loan.objects.create(title=title, point=point)
        return redirect('/add_loans')
    return render(request,'add_loan.html',{'data':data})
def loans_delet(request,id):
    data = Loan.objects.get(id = id)
    data.delete()
    return redirect('/add_loans')

def grant_delet(request,id):
    data = Grant.objects.get(id = id)
    data.delete()
    return redirect('/add_grants')

def add_grants(request):
    data = Grant.objects.all()
    if request.method == 'POST':
        title = request.POST.get('titile')
        point = request.POST.get('point')
        Grant.objects.create(title=title, point=point)
        return redirect('/add_grants')
    return render(request,'add_grants.html',{'data':data})

def more_informations(request):
    return render(request,'more_information.html')


def mentor_records(request):
    data = CustomUser.objects.filter(verifi = True)
    return render(request,'mentor_records.html',{'data':data})
    

from django.contrib.auth.hashers import make_password
def accpect_mentor(request,id):
    data = CustomUser.objects.get(id = id) #3
    if request.method == 'POST':
        data.verifi = True 
        data.save()
        return redirect('/add_mendor')
    return render(request,'accpect_mentor.html',{'data':data})

def add_mendor(request):
    data = CustomUser.objects.filter(verifi = False)   
    return render(request,'add_mendor.html',{'data':data})


def student_signup(request):
    data = 'Student Signup'
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        gender = request.POST['gender']
        email = request.POST['emal']
        contact = request.POST['number']
        clg_name = request.POST['c_name']
        username = request.POST['uname']
        password1 = request.POST['psw']
        password2 = request.POST['re_psw']
        if CustomUser.objects.filter(username = username):
            messages.error(request,'username is already taken')
            return redirect('/')     
        if password1 == password2:
            CustomUser.objects.create_user(username=username, password=password1, user_type=1,name = name,age = int(age),gender = gender,email = email,contact = int(contact),class_name = clg_name)
            return redirect('/login')
        
    return render(request, 'signup.html',{'data':data})

def faculty_signup(request):
    data = 'Faculty Signup'
    if request.method == 'POST':
        username = request.POST['uname']
        password1 = request.POST['psw']
        password2 = request.POST['re_psw']
        email = request.POST['email']
        number =  request.POST['number']
        qly =  request.POST['qly']
        cls = request.POST['cls']
        fee = request.POST['fee']
        if CustomUser.objects.filter(username = username):
            messages.error(request,'username is already taken')
            return redirect('/')  
        if password1 == password2:
            user = CustomUser.objects.create_user(username=username, password=password1, user_type=2,email = email,contact = number,qualification = qly,class_name = cls,fee = fee,verifi = False)
            return redirect('/login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('/admin_signup')
    return render(request, 'fac_signup.html',{'data':data})



def admin_signup(request):
    data = 'Admin Signup'
    if request.method == 'POST':
        username = request.POST['uname']
        password1 = request.POST['psw']
        password2 = request.POST['re_psw']
        pin = request.POST['pin'] #1234
        
        if int(pin) != 1234:
            messages.error(request, 'Invalid PIN')
            return redirect('/admin_signup')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken')
            return redirect('/admin_signup')
        
        

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('/admin_signup')
        
        CustomUser.objects.create_user(username=username, password=password1, user_type=3)
        return redirect('/login')
    
    return render(request, 'admin_signup.html', {'data': data})

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password1 = request.POST['psw']
        user = authenticate(username=username, password=password1)
        if user is not None:  
            login(request, user)
            if user.user_type == 1:
                return redirect('student_dashboard')
            elif user.user_type == 2:
                if user.verifi == 'True':
                    return redirect('faculty_dashboard')
                else:
                    messages.error(request, 'Request declined.')
                    return redirect('/login')          
            elif user.user_type == 3:
                return redirect('admin_dashboard')
    return render(request, 'login.html')

def logoutt(request):
    logout(request)
    return redirect('/')


@login_required
def student_dashboard(request):
    return render(request, 'student_dashboard.html')

@login_required
def faculty_dashboard(request):
    return render(request, 'faculty_dashboard.html')

@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


def index(request):        
    return render(request,'index.html')

def common_signup(request):        
    return render(request,'common_signup.html')

