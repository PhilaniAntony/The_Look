from django.contrib.auth.forms import  UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import  Customer, Newsletter, ContactDetails

class CreateUserForm(UserCreationForm):
    class  Meta :
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class NewsletterForm(ModelForm):
    class Meta :
        model = Newsletter
        fields = ['email']
        

class ContactDetailsForm(ModelForm):
    class Meta :
        model = ContactDetails
        fields = '__all__'