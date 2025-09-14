from django import forms
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    studentid = forms.CharField(max_length=10)
    
    class Meta:
        model = User
        fields = ['username', 'studentid', 'password']
    def clean_studentid(self):
        studentid = self.cleaned_data['studentid']
        if Profile.objects.filter(studentid=studentid).exists():
            raise forms.ValidationError("This student ID is already registered.")
        return studentid

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Profile.objects.create(user=user, studentid=self.cleaned_data['studentid'])
        return user