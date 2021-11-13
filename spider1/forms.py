# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit
from django import forms
from .models import *
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import password_validation
#from autho.models import Users
from django.contrib.auth.hashers import make_password
# Create your forms here.
#validators
def validate_my_email(email):
    try:
        validate_email(email)
        return email
    except forms.ValidationError:
        print("Email errors")
        raise forms.ValidationError(("Your email is invalid"))

class RegistrationForm(forms.Form):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-sm'}), label="First Name")
    surname =forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sm'}), label='Surname')
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-sm'}), label="Last Name")
    dob=forms.CharField(widget=forms.TextInput(attrs={'class': 'datepicker form-control input-sm' ,'data-type': 'dateIso'}), label="DOB")
    phone =forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sm'}), label='Phone')
    email=forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control input-sm'}), label="Email", validators = [validate_my_email])
    national_id=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-sm'}), label="National Id / Passport")
    date_time_of_registration =forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sm'}), label='Date of Reg')
    gender=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-sm' }), label="Gender")
    marital_status=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-sm'}), label="Marital Status")
    patient_no =forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sm'}), label='Patient No')
    city=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-sm'}), label="City")
    village = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control input-sm'}), label="Village")
#forms
class TestForm1(forms.Form):
    name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Name",validators=[validate_my_email])
    age =forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Age')
    text=forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label="Text")
# class TestForm2(forms.Form):
#     name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Name")
#     age =forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Age')
#     text=forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label="Text")
#     def __init__(self, *args, **kwargs):
#        super(TestForm2, self).__init__(*args, **kwargs)
#        self.helper = FormHelper()
#        self.helper.form_id = 'id-test-form'
#        self.helper.form_method = 'post'
#        self.helper.form_action = 'add_crispy_test'
#        self.helper.add_input(Submit('submit', 'save'))

# class ModelTestForm1(forms.ModelForm):
#     class Meta:
#         model = Test
#         fields = ('name','age', 'text',)