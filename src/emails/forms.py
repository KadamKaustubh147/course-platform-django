from django import forms

from .models import Email, EmailVerificationEvent

from . import css, services

# A widget is Django’s representation of an HTML input element. The widget handles the rendering of the HTML, and the extraction of data from a GET/POST dictionary that corresponds to the widget.


# class CommentForm(forms.Form):
#     name = forms.CharField()
#     url = forms.URLField()
#     comment = forms.CharField(widget=forms.Textarea)

# forms.Form or forms.ModelForm

class EmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs = {
                "id": "email-login-input",
                "class": css.EMAIL_INPUT_CSS,
                "placeholder": "youremail@email.com"
            }
        )
    )
    # class Meta:
    #     model = EmailVerificationEvent
    #     fields = ['email']

    # this method will run automatically
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Email.objects.filter(email=email, active=False)
        # agar active nai hai toh return inactive email

        verified = services.verify_email()
        if verified:
            raise forms.ValidationError("Inactive email please try again")
        return email