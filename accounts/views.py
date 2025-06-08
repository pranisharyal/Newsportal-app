from django.shortcuts import redirect, render
from django.contrib.auth import login
from .forms import RegistrationForm

# Create your views here.

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(
                "accounts:login"
            )
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})
