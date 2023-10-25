from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from users.forms import CustomUserCreationForm
from django.http import JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


#TO FIX MISSING CSRF PROTECTION SIMPLY REMOVE THESE @csrf_exempt DECORATORS
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


#THIS FEATURE DOESNT REQUIRE THE USER TO BE LOGGED IN. TO FIX IT SIMPLY REMOVE THE COMMENT FROM THE @login_required DECORATOR
#@login_required
@csrf_exempt
def user_url(request):
    if request.method == "GET":
        return render(request, "users/userurl.html")
    
    if request.method == "POST":
        url = request.POST.get("url")
    #HERE WE ARE FIXING THIS FEATURE TO BE MORE SAFE BY ONLY ALLOWING URLS FROM CERTAIN WEBSITES

        #allowed_websites = ["safewebsite.fi", "youcantrustthis.com", "safeforcats.org"] (MAKE A LIST OF ALLOWED WEBSITES)

        #NOW CHECKING IF THE URL IS OK, IF NOT THEN RETURN

        #if url not in allowed_websites:
            #return JsonResponse({"error": "url is not from an allowed website"})
        
        #ALTERNATIVELY WE COULD ALSO CHECK IF THE URL STARTS WITH "http://" OR "https://"
        try:
            response = requests.get(url)
            content = response.text
        except requests.exceptions.RequestException as e:
            content = str(e)

        return JsonResponse({"result": content})

    return JsonResponse({"error": "POST or GET request required"})
