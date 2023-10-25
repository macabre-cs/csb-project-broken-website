from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from users.forms import CustomUserCreationForm
#from django.contrib.auth.decorators import permission_required, login_required

def dashboard(request):
    return render(request, "users/dashboard.html")

def register(request):
    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            #HERE WE ARE GIVING A NORMAL USER ACCESS TO ADMIN STUFF

            user = form.save(commit=False)
            user.is_superuser = True
            user.is_staff = True
            user.save()

            #TO FIX THIS THE CODE SHOULD JUST BE:
            #user = form.save()
            #SO YOU SHOULD DELETE LINES
            #user.is_superuser = True
            #user.is_staff = True
            #user.save()

            login(request, user)
            return redirect(reverse("dashboard"))
    else:
        form = CustomUserCreationForm()
    return render(request, "users/dashboard.html", context={"form":form})
