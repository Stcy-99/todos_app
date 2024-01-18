from django.shortcuts import render,redirect
from django.views.generic import View
from reminder.forms import UserForm,SignInForm,TodoForm
from django.contrib.auth import authenticate,login,logout
from reminder.models import Todos
from django.utils.decorators import method_decorator
from django.contrib import messages

def owner_permision_required(fn):
    def wrapper(request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_object=Todos.objects.get(id=id)
        if todo_object.user != request.user:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper
def Signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=UserForm()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=UserForm(request.POST)
        if form.is_valid():
            form.save()
            print("Account Created")
            return redirect("register")
        else:
            print("Failed")
            return render(request,"register.html",{"form":form})

        
        
class SignInView(View):

    def get(self,request,*args,**kwargs):
        form=SignInForm()
        return render(request,"signin.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=SignInForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=uname,password=pwd)

            if user_object:
                login(request,user_object)
                print("Login Success")
                return redirect("index")
        print("invalid Credentials")
        return render(request,"signin.html",{"form":form})

decs=[Signin_required,owner_permision_required]

@method_decorator(Signin_required,name="dispatch")
class IndexView(View):
    def get(self,request,*args,**kwrags):
        form=TodoForm()
        qs=Todos.objects.filter(user=request.user).order_by("status")
        return render(request,"index.html",{"form":form,"data":qs})
    def post(self,request,*args,**kwargs):
        form=TodoForm(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            return redirect("index")
        else:
            return render(request,"index.html",{"form":form})
        

#localhost:8000/todos/{id}/remove/
@method_decorator(decs,name="dispatch")       
class DeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Todos.objects.filter(id=id).delete()
        return redirect("index")
    
#localhost:8000/todos/{id}/change/
@method_decorator(decs,name="dispatch") 
class ChangeView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_object=Todos.objects.get(id=id)
        if todo_object.status==True:
            todo_object.status=False
            todo_object.save()
        else:
            todo_object.status=True
            todo_object.save()
        return redirect("index")


@method_decorator(Signin_required,name="dispatch") 
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")

            
