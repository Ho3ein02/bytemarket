from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class PhoneForm(forms.Form):
    phone = forms.CharField(max_length=11)

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if len(phone) != 11:
            raise forms.ValidationError('شماره نامعتبر است.')

        if not phone.isdigit():
            raise forms.ValidationError('شماره فقط می تواند شامل اعداد باشد.')

        if not phone.startswith('09'):
            raise forms.ValidationError('شماره باید با 09 شروع شود.')

        return phone


class ShopUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['phone', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser']


class ShopUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ['phone', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email']
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        
        if User.objects.filter(phone=phone).exclude(id=self.instance.pk).exists():
            raise forms.ValidationError('شماره وارد شده مجاز نیست')
        else:
            return phone
    
    def clean_email(self):
        email = self.cleaned_data['email']
        
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('ایمیل قبلا وارد شده است')
        else:
            return email
