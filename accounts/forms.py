from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Profile
from .models import LostAndFound

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'address-input'}),
        required=False
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone_number', 'address')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number', 'address')

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

class LostAndFoundForm(forms.ModelForm):
    class Meta:
        model = LostAndFound
        fields = ['title', 'description', 'status', 'contact_info']