from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings


expense_type_options = [
        ('f&b', 'Food and Drinks'),
        ('accoms', 'Accomodations'),
        ('taxi', 'Taxi'),
        ('transport', 'Transportation'),
        ('flight', 'Flight tickets'),
        ('shopping', 'Shopping'),
        ('groceries', 'Groceries'),
        ('donatation', 'Donation'),
        ('entertainment', 'Entertainment'),
        ('auto', 'Auto and Parking'),
        ('bills', 'Bills'),
        ('fees', 'Fees'),
        ('health', 'Heath'),
        ('insurance', 'Insurance'),
        ('personalcare', 'Personal care'),
        ]


class Trip(models.Model):
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    budget = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)
    depart_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)
    groups = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Group', related_name='trip_group')

    def __str__(self):
        return self.title


class Group(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Expenses(models.Model):
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE)
    expense = models.DecimalField(max_digits=100, decimal_places=2)
    # expense_type = models.OneToOneField('ExpenseType', on_delete=models.CASCADE)
    expense_type = models.CharField(max_length = 50, choices=expense_type_options)
    description = models.CharField(max_length = 50)
    transaction_date = models.DateTimeField(null=True, blank=True)

# class ExpenseType(models.Model):
#     types = models.CharField(max_length = 50, choices=expense_type_options)


class Tags(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    tag = models.CharField(max_length = 50)

    def __str__(self):
        return Tags.tag

class Blog(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    title = models.CharField(max_length = 150)
    post = models.TextField()
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Comment', related_name='comments_owned')

class Comment(models.Model):
    text = models.TextField()
    blogpost = models.ForeignKey('Blog', on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'
