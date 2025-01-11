from django.shortcuts import render
from django.conf import settings

from emails.forms import EmailForm

EMAIL_ADDRESS = settings.EMAIL_ADDRESS

def home(request, *args, **kwargs):
    template_name = "home.html"
   
    print(request.POST) 
    form = EmailForm(request.POST or None)
    
    context = {
        "form": form,
        "message": ""
    }
    
    if form.is_valid():
        obj = form.save()
        print("start")
        print(obj)
        print("end")
        context['form'] = EmailForm()
        context['message'] = f"Success! Check your inbox for verification from {EMAIL_ADDRESS}"
    else:
        print(form.errors)
    return render(request, template_name, context)