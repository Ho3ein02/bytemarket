from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


# Form for phone number input and validation the phone number
class PhoneForm(forms.Form):
    phone = forms.CharField(max_length=11)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        
        # Validate the length of the phone number
        if len(phone) != 11:
            raise forms.ValidationError('شماره نامعتبر است.')
        
        # Validate that the phone number contains only digits
        if not phone.isdigit():
            raise forms.ValidationError('شماره فقط می تواند شامل اعداد باشد.')

        # Validate that the phone number starts with '09'
        if not phone.startswith('09'):
            raise forms.ValidationError('شماره باید با 09 شروع شود.')

        return phone


# Form for createing a new user
class ShopUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['phone', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser']
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        
        # Validate the length of the phone number
        if len(phone) != 11:
            raise forms.ValidationError('شماره نامعتبر است.')
        
        # Validate that the phone number contains only digits
        if not phone.isdigit():
            raise forms.ValidationError('شماره فقط می تواند شامل اعداد باشد.')

        # Validate that the phone number starts with '09'
        if not phone.startswith('09'):
            raise forms.ValidationError('شماره باید با 09 شروع شود.')

        return phone


# Form for changing an existing user
class ShopUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ['phone', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser']
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        
        # Validate the length of the phone number
        if len(phone) != 11:
            raise forms.ValidationError('شماره نامعتبر است.')
        
        # Validate that the phone number contains only digits
        if not phone.isdigit():
            raise forms.ValidationError('شماره فقط می تواند شامل اعداد باشد.')

        # Validate that the phone number starts with '09'
        if not phone.startswith('09'):
            raise forms.ValidationError('شماره باید با 09 شروع شود.')

        return phone


# Form for changing user information
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email']
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        
        # Validate that the phone number is unique, excluding the current instance
        if User.objects.filter(phone=phone).exclude(id=self.instance.pk).exists():
            raise forms.ValidationError('شماره وارد شده مجاز نیست')
        
        # Validate the length of the phone number
        if len(phone) != 11:
            raise forms.ValidationError('شماره نامعتبر است.')
        
        # Validate that the phone number contains only digits
        if not phone.isdigit():
            raise forms.ValidationError('شماره فقط می تواند شامل اعداد باشد.')

        # Validate that the phone number starts with '09'
        if not phone.startswith('09'):
            raise forms.ValidationError('شماره باید با 09 شروع شود.')

        return phone
    
    def clean_email(self):
        email = self.cleaned_data['email']
        
        # Validate that the email is unique, excluding the current instance
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('ایمیل قبلا وارد شده است')
        return email
