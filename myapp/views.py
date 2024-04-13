from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate
from django.contrib import messages
from .models import *
from django.http import Http404
from datetime import datetime
import os

# Create your views here.


def index(request):
    return render(request, "index.html")


def reg(request):
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        gender = request.POST["gender"]
        image = request.FILES["image"]
        password = request.POST["password"]

        print(email)
        if Login.objects.filter(username=email).exists():
            messages.error(request, "Email or password already taken")
        else:
            logUser = Login.objects.create_user(
                username=email,
                password=password,
                userType="User",
                viewPass=password,
                is_active=1,
            )
            logUser.save()

            userReg = Userreg.objects.create(
                name=name,
                email=email,
                phone=phone,
                image=image,
                gender=gender,
                loginid=logUser,
            )
            userReg.save()
            messages.error(request, "Successfully created")
            return redirect("/")
    return render(request, "reg.html")


def quiz_creator(request):
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        # gender = request.POST["gender"]
        image = request.FILES["image"]
        password = request.POST["password"]

        print(email)
        if Login.objects.filter(username=email).exists():
            messages.error(request, "Email or password already taken")
        else:
            logUser = Login.objects.create_user(
                username=email,
                password=password,
                userType="Creator",
                viewPass=password,
                is_active=1,
            )
            logUser.save()

            userReg = Creator.objects.create(
                name=name,
                email=email,
                phone=phone,
                image=image,
                # gender=gender,
                loginid=logUser,
            )
            userReg.save()
            messages.error(request, "Successfully created")
            return redirect("/")
    return render(request, "creator_reg.html")


def login(request):
    if request.POST:
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(username=email, password=password)

        if user is not None:
            if user.userType == "Admin":
                messages.success(request, "Login Success")
                return redirect("/admin_home")

            elif user.userType == "User":
                request.session["uid"] = user.id
                request.session["email"] = user.username
                messages.success(request, "Login Success")
                return redirect("/user_home")

            elif user.userType == "Creator":
                request.session["uid"] = user.id
                request.session["email"] = user.username
                messages.success(request, "Login Success")
                return redirect("/creator_home")

            else:
                messages.error(request, "User type not defined")

        else:
            messages.error(request, "You are not approved yet ")
    return render(request, "log.html")


def user_home(request):
    uid = request.session["uid"]
    Cid = Userreg.objects.filter(loginid=uid)
    return render(request, "User/index3.html", {"view": Cid})


def admin_home(request):
    return render(request, "Admin/index.html")


def creator_home(request):
    uid = request.session["uid"]
    Cid = Creator.objects.filter(loginid=uid)

    # print("Name :" ,Cid.name)
    return render(request, "Creator/index.html", {"view": Cid})


def adm_view_users(request):
    view = Userreg.objects.all()
    return render(request, "Admin/view_users.html", {"view": view})


def adm_view_creators(request):
    view = Creator.objects.all()
    return render(request, "Admin/view_creators.html", {"view": view})


def udp(request):
    dele=Question.objects.filter(id=10).delete()
    return HttpResponse("success",)


def add_question(request):
    qcid=request.GET.get("qid")
    print(qcid, "Question")
    Qcid=Quiz_category.objects.get(id=qcid)
    
    uid = request.session["uid"]
    Cid = Creator.objects.get(loginid=uid)
    if request.method == "POST":
        question = request.POST["question"]
        option1 = request.POST["op1"]
        option2 = request.POST["op2"]
        option3 = request.POST["op3"]
        option4 = request.POST["op4"]
        file = request.FILES.get("file")
        answer = request.POST["answer"]
        
        if Question.objects.filter(qcid=Qcid).count() >= 5:
            messages.error(request, "You have reached the limit of 5 questions")
            return redirect(f"/add_question?qid={qcid}")
        else:

            if file:
                ins = Question.objects.create(
                    question=question,
                    op1=option1,
                    op2=option2,
                    op3=option3,
                    op4=option4,
                    answer=answer,
                    cid=Cid,
                    image=file,
                    qcid=Qcid
                )
                ins.save()
                messages.success(request, "Question Added Successfully")
                return redirect(f"/add_question?qid={qcid}")
            else:
                ins = Question.objects.create(
                    question=question,
                    op1=option1,
                    op2=option2,
                    op3=option3,
                    op4=option4,
                    answer=answer,
                    cid=Cid,
                    qcid=Qcid
                )
                ins.save()
                messages.success(request, "Question Added Successfully")
                return redirect(f"/add_question?qid={qcid}")

    return render(request, "Creator/add_question.html")


def creator_view_quiz(request):
    uid = request.session["uid"]
    Cid = Creator.objects.get(loginid=uid)
    view = Question.objects.filter(cid=Cid)
    return render(request, "Creator/view_question.html", {"view": view})


def user_view_quiz(request):
    view = Question.objects.all()
    return render(request, "User/view_question.html", {"view": view})

def answe_to_question(request):
    uid = request.session["uid"]
    Uid = Userreg.objects.get(loginid=uid)
    qcid = request.GET.get('qcid')
    cid = request.GET.get('cid')
    Cid = Creator.objects.get(loginid=cid)
    Qcid = Quiz_category.objects.get(id=qcid)
    view = Question.objects.filter(qcid=qcid)
    questions = Question.objects.all()
    
    if request.method == "POST":
        answer=request.POST.get("answer")
        Questine=Question.objects.get(id=answer)
        score = 0
        mark = 0
        for question in questions:
            question_id = str(question.id)
            selected_answer = request.POST.get("question_" + question_id)
            print(selected_answer)
            if selected_answer is not None:
                parts = selected_answer.split('/')
                selected_answer = parts[0]
                correct_answer = question.answer
                if selected_answer == correct_answer:
                    score += 1
                    mark = score * 5
            else:
                continue  

        print(mark, "Score")     
        print("answered Question", score, "/5")
                
        ins = Answered_question.objects.create(answer=score, mark=mark, cid=Cid, qcid=Qcid, uid=Uid,question=Questine)
        ins.save()
        return redirect(f"/score?ansis={ins.id}&qcid={qcid}")
        
    return render(request, "User/answe_to_question.html", {"view": view})


def add_question_category(request):
    uid = request.session["uid"]
    Cid = Creator.objects.get(loginid=uid)
    view=Quiz_category.objects.all()
    if request.method == "POST":
        category = request.POST["category"]
        ins = Quiz_category.objects.create(cid=Cid,category=category)
        ins.save()
        messages.success(request, "Category Added Successfully")
        return redirect("/add_question_category")
    
    return render(request, "Creator/add_question_category.html",{"view": view})


def delete_question_category(request):
    qcid=request.GET.get("qcid")
    Qcid=Quiz_category.objects.filter(id=qcid).delete()
    messages.success(request, "Category Deleted ")
    return redirect("/add_question_category")
    
def user_view_quiz_category(request):
    Qcid=Quiz_category.objects.all()
    return render(request, "User/view_category.html",{"view":Qcid})


def delete_question(request):

    qid=request.GET.get("qid")
    dele=Question.objects.filter(id=qid).delete()
    messages.success(request,"Question Deleted")
    return redirect("/creator_view_quiz")

def score(request):
    qcid=request.GET.get("qcid")
    
    uid = request.session["uid"]
    Uid = Userreg.objects.get(loginid=uid)
    ansid=request.GET.get("ansis")
    ans=Answered_question.objects.filter(id=ansid,uid=Uid)
    answers=Question.objects.filter(qcid=qcid)
    print("Qcid : ",answers)
    
    return render(request, "User/score.html",{"view":ans,"ans":answers})

def view_answers(request):
    uid = request.session["uid"]
    Uid = Userreg.objects.get(loginid=uid)
    view=Answered_question.objects.filter(uid=Uid)
    return render(request, "User/view_answers.html", {"view":view})


def delete_creator(request):
    cid=request.GET.get('cid')
    Cid=Creator.objects.filter(loginid=cid).delete()
    
    return HttpResponse("<script>alert('creator Deleted');window.location.reload();</script>")

def delete_answer(request):
    aid=request.GET.get('aid')
    Cid=Answered_question.objects.filter(id=aid).delete()
    
    return HttpResponse("<script>alert('Answer Deleted');window.location='/view_answers';</script>")

def approve_edu(request):
    eid=request.GET.get('cid')
    Eid=Creator.objects.get(loginid=eid)
    Up=Login.objects.filter(id=Eid.id).update(is_active=1)
    
    return HttpResponse("<script>alert('Educator Approved');window.location='/adm_view_creators';</script>")