from django import forms
from tracker.models import Trip, Expenses, expense_type_options

class DateInput(forms.DateInput):
    input_type = 'date'


class CreateTripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['title', 'budget', 'depart_date', 'return_date']

class ShareTripForm(forms.Form):
    username = forms.CharField(required=True, max_length=200, min_length=1, strip=True)

class AddExpenseForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ['description', 'expense', 'expense_type', 'transaction_date']
        widgets = {'transaction_date' : DateInput()}

    def clean(self):
        cleaned_data = super(AddExpenseForm, self).clean()
        if not cleaned_data.get('transaction_date'):
            cleaned_data['transaction_date'] = None
        return cleaned_data
