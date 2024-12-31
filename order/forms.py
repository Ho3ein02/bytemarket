from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['phone', 'first_name', 'last_name', 'postal_code', 'address', 'province', 'city']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        
        if len(phone) != 11:
            raise forms.ValidationError('شماره تلفن نامعتبر است.')
        
        if not phone.isdigit():
            raise forms.ValidationError('شماره تلفن فقط می تواند شامل عدد باشد.')
        
        if not phone.startswith('09'):
            raise forms.ValidationError('شماره تلفن باید با 09 شروع شود.')
        
        return phone
    
    def clean_postal_code(self):
        postal_code = self.cleaned_data['postal_code']
        
        if not postal_code.isdigit():
            raise forms.ValidationError('کد پستی فقط شامل عدد می تواند باشد.')
        
        return postal_code
    
    def clean_province(self):
        province = self.cleaned_data['province']
        
        if not province:
            raise forms.ValidationError('این فیلد نمی تواند خالی باشد')
        return province
    
    def clean_city(self):
        city = self.cleaned_data['city']
        
        if not city:
            raise forms.ValidationError('این فیلد نمی تواند خالی باشد')
        return city
