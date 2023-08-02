from time import time
from unicodedata import name
from django.shortcuts import render, HttpResponse
from Home.models import Problem, Submission, TestCases, User
from django.contrib import messages
from datetime import datetime
from django.shortcuts import render, HttpResponse, get_object_or_404

from Home.runcode import RunCode

def start(request):
    return render(request,'startpage.html')

def home(request,user_name):
    user = User.objects.get(username=str(user_name))
    types = Problem.objects.values('type').distinct()
    rank = User.objects.all().filter(problems_solved__gt=user.problems_solved).count() + 1
    return render(request,'homepage.html',{'user':user,'types':types,'rank':rank})

def signin(request):
    if request.method == "GET":
        email = request.GET.get('email')
        password = request.GET.get('password')

        user_list = User.objects.filter(email=str(email),password=str(password))
        if len(user_list) > 0:
            user = user_list[0]
            types = Problem.objects.values('type').distinct()
            return render(request,'homepage.html',{'user':user,'types':types})
        if password is not None:
            messages.error(request,'Incorrect Email or Password') 
    
    return render(request,'startpage.html')

def signup(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2 and password1 is not None:
            messages.success(request,'Passwords don\'t match.')
        else:
            user = User(name=name,email=email,password=password1)
            user.save()
            messages.success(request,'Your Account has been created.')

    return render(request,'signup.html')

def problems(request, user_name=None):
    user = None
    rank = None

    if user_name is not None:
        try:
            user = User.objects.get(username=str(user_name))
            rank = User.objects.all().filter(problems_solved__gt=user.problems_solved).count() + 1
        except User.DoesNotExist:
            pass

    problems = Problem.objects.all()
    types = Problem.objects.values('type').distinct()
    return render(request, 'problems.html', {'user': user, 'problems': problems, 'types': types, 'rank': rank})




def problem_search(request,user_name):
    if request.method == "POST":
        search_string = request.POST.get('search')
        problems = Problem.objects.filter(name__icontains=search_string)
    else:
        problems = Problem.objects.all()
    user = User.objects.get(username=str(user_name))
    rank = User.objects.all().filter(problems_solved__gt=user.problems_solved).count() + 1
    types = Problem.objects.values('type').distinct()
    return render(request,'problems.html',{'user':user,'problems':problems,'types':types,'rank':rank})

def problems_typeSpecific(request,user_name,type):
    user = User.objects.get(username=str(user_name))
    problems = Problem.objects.filter(type=str(type))
    rank = User.objects.all().filter(problems_solved__gt=user.problems_solved).count() + 1
    types = Problem.objects.values('type').distinct()
    return render(request,'problems.html',{'user':user,'problems':problems,'types':types,'rank':rank})

def problems_difficuiltySpecific(request,user_name,difficuilty):
    user = User.objects.get(username=str(user_name))
    problems = Problem.objects.filter(difficuilty=str(difficuilty))
    rank = User.objects.all().filter(problems_solved__gt=user.problems_solved).count() + 1
    types = Problem.objects.values('type').distinct()
    return render(request,'problems.html',{'user':user,'problems':problems,'types':types,'rank':rank})

def problem_description(request,user_name,id):
    user = User.objects.get(username=str(user_name))
    problem = Problem.objects.get(id=id)
    rank = User.objects.all().filter(problems_solved__gt=user.problems_solved).count() + 1
    return render(request,'problem_desc.html',{'user':user,'problem':problem,'rank':rank})

def submit(request,user_name,id):
    user = User.objects.get(username=str(user_name))
    problem = Problem.objects.get(id=id)
    curr_testcase = TestCases.objects.get(problem=problem)
    rank = User.objects.all().filter(problems_solved__gt=user.problems_solved).count() + 1
    
    if request.method == 'POST':
        code = request.POST.get('textarea')
        lang_code = request.POST.get('language')
        verdict = ""
        output_testcases = []
        compiled_testcases = []

        language = {'1' : "C++", '2' : "Java", '3' : "Python"}
        ext = {'1' : "cpp", '2' : "java", '3' : "py"}

        template_path = "static/templates/problem"+str(id)+"_"+ext[lang_code]+".txt"

        with open(curr_testcase.input,'r') as f:
            input = f.read()

        p = RunCode(language[lang_code],template_path,code)
        error,compiled_testcases = p.run_code(input)
        print(str(error))

        with open(curr_testcase.output,'r') as f:
            output_testcases = f.read().split('\n')
        
        ans = -1
        ans = match_testcases(output_testcases,compiled_testcases,ans)
        if ans==0:
            verdict = "Correct Answer"
            solved_problems = user.problems_solved
            user.problems_solved = solved_problems + 1
            user.save()
        elif ans > 0:
            verdict = "Failed at Testcase " + str(ans)
        else:
            verdict = "Code Error"

        submission = Submission(user=user,problem=problem,code=code,verdict=verdict,time=datetime.now())
        submission.save()
        
    return render(request,'problem_desc.html',{'user':user,'problem':problem,'rank':rank,'ans':ans,'error':str(error)})

def match_testcases(output_testcases,compiled_testcases,ans):
    if len(output_testcases) != len(compiled_testcases):
        return ans
    for i in range(0,len(output_testcases)-1):
        out = str(output_testcases[i]).rstrip()
        comp = str(compiled_testcases[i]).rstrip()
        if out != comp:
            return i+1
    return 0

def submissions(request,user_name):
    user = User.objects.get(username=str(user_name))
    submissions = Submission.objects.filter(user=user).order_by('-time')
    rank = User.objects.all().filter(problems_solved__gt=user.problems_solved).count() + 1
    return render(request,'submissions.html',{'user':user,'submissions':submissions,'rank':rank})

def leaderboard(request):
    user = User.objects.order_by('-problems_solved')
    return render(request,'leaderboard.html',{'user':user})