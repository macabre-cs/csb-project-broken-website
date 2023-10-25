from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from users.forms import CustomUserCreationForm
from django.http import JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def dashboard(request):
    return render(request, "users/dashboard.html")

@csrf_exempt
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

#STUFF LIKE THIS SHOULD NOT BE IN THIS CODE
#DANGERRRRRRRRRRRR

#fix, allowed domains todo hehe
@csrf_exempt
def user_url(request):
    if request.method == "GET":
        return render(request, "users/userurl.html")
    if request.method == "POST":
        url = request.POST.get("url")
        try:
            response = requests.get(url)
            content = response.text
        except requests.exceptions.RequestException as e:
            content = str(e)

        return JsonResponse({"result": content})

    return JsonResponse({"error": "POST or GET request required"})
    #return render(request, "userurl.html")
