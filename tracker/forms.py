from django import forms
from tracker.models import Trip, Expenses, Blog, Comment

class DateInput(forms.DateInput):
    input_type = 'date'


class CreateTripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['title', 'budget', 'depart_date', 'return_date']
        widgets = {'depart_date' : DateInput(), 'return_date' : DateInput()}

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

class CreateBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'post']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']