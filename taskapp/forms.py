from django import forms

class LoginForm(forms.Form):
    role = forms.ChoiceField(
        max_length=10,
        choices=[('employee', 'Employee'), ('manager', 'Manager'), ('client', 'Client')]
    )
    name = forms.CharField(max_length=150)
    email = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150, widget=forms.PasswordInput())