from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    contact_no = forms.CharField(max_length=15, required=True)
    profile_picture = forms.ImageField(required=False)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.contact_no = self.cleaned_data.get('contact_no')
        user.profile_picture = self.cleaned_data.get('profile_picture')
        user.save()
        return user
