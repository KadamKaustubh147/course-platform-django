from django.shortcuts import render
from django.conf import settings

from emails.forms import EmailForm
from emails.models import Email, EmailVerificationEvent

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
        email_val = form.cleaned_data.get('email')
        # obj = form.save()
        # email_obj, created = Email.objects.get_or_create(email=obj.email)
        email_obj, created = Email.objects.get_or_create(email=email_val)
        EmailVerificationEvent.objects.create(
            parent=email_obj,
            email=email_val
        )
        # print(obj)
        context['form'] = EmailForm()
        context['message'] = f"Success! Check your inbox for verification from {EMAIL_ADDRESS}"
    else:
        print(form.errors)
    return render(request, template_name, context)