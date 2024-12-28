from django import forms
from .models import Brand, Category


class ProductFilterForm(forms.Form):
    available = forms.BooleanField(required=False)
    max_price = forms.DecimalField(min_value=0, required=False)
    min_price = forms.DecimalField(min_value=0, required=False)

    # Field for checkbox
    brand = forms.ModelMultipleChoiceField(queryset=Brand.objects.all(),
                                           widget=forms.CheckboxSelectMultiple,
                                           required=False)

    # Field for checkbox
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                              widget=forms.CheckboxSelectMultiple,
                                              required=False)


class SearchForm(forms.Form):
    query = forms.CharField(required=False)


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)
    parent = forms.CharField()
