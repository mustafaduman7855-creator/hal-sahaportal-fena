from django import forms
from .models import PublishRequest, User, Facility
from django.contrib.auth.forms import AuthenticationForm

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    facility_code = forms.CharField()

    class Meta:
        model = User
        fields = ['email','password']

    def clean_facility_code(self):
        code = self.cleaned_data['facility_code']
        if not Facility.objects.filter(code=code).exists():
            raise forms.ValidationError('Geçersiz tesis kodu')
        return code

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        user.facility = Facility.objects.get(code=self.cleaned_data['facility_code'])
        if commit:
            user.save()
        return user

class PublishRequestForm(forms.ModelForm):
    consent = forms.BooleanField(required=True)
    class Meta:
        model = PublishRequest
        fields = ['match_date','start_time','end_time','consent']
        widgets = {
            'match_date': forms.DateInput(attrs={'type':'date'}),
            'start_time': forms.TimeInput(attrs={'type':'time'}),
            'end_time': forms.TimeInput(attrs={'type':'time'}),
        }

class LoginForm(AuthenticationForm):
    username = forms.EmailField()
