from django import forms
from tracker.models import Trip, Expenses, expense_type_options

class CreateTripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['title', 'budget', 'depart_date', 'return_date']
    # title = forms.CharField(required=True, max_length=200, min_length=2, strip=True)
    # budget = forms.DecimalField(max_digits=100, decimal_places=2, required=False)
    # depart_date = forms.DateTimeField(required=False)
    # return_date = forms.DateTimeField(required=False)

class ShareTripForm(forms.Form):
    username = forms.CharField(required=True, max_length=200, min_length=1, strip=True)

class AddExpenseForm(forms.Form):
    description = forms.CharField(required=True, max_length=50, strip=True)
    expense = forms.DecimalField(max_digits=100, decimal_places=2, required=True)
    expense_type = forms.ChoiceField(choices=expense_type_options)
    transaction_date = forms.DateTimeField(required=False)