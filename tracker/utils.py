from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse
from tracker.models import Trip, Group, Expenses, Tags, Blog, Comment

class UpdateBaseClass(LoginRequiredMixin, DetailView):
    def __init__(self, model, modelform, modelname):
        self.model = model
        self.modelform = modelform
        self.modelname = modelname

    def get(self, request, pk, **kwargs):
        if request.is_ajax():
            return JsonResponse({"message":"success"})
        else:
            return Http404('Access denied')

    def post(self, request, pk, **kwargs):
        if request.is_ajax():
            id_key = kwargs['expense_id'] if self.modelname == 'expense' else pk
            instance = self.model.objects.get(pk=id_key)
            form = self.modelform(request.POST or None, instance=instance)
            if form.is_valid():
                instance = form.save()
                return JsonResponse({"message": "success"})
            else:
                return JsonResponse({"message": "Validation failed"})
        else:
            return JsonResponse({"message": "Wrong request"})

class DeleteBaseClass(LoginRequiredMixin, DetailView):
    def __init__(self, model, modelname):
        self.model = model
        self.modelname = modelname

    def get(self, request, pk, **kwargs):
        if request.is_ajax():
            return JsonResponse({"message":"success"})
        else:
            return Http404('Access denied')

    def post(self, request, pk, **kwargs):
        if request.is_ajax():
            if self.modelname == 'expense':
                id_key = kwargs['expense_id']
            elif self.modelname == 'blog':
                id_key = kwargs['blog_id']
            elif self.modelname == 'comment':
                id_key = kwargs['comment_id']
            else:
                id_key = pk

            instance = get_object_or_404(self.model, pk=id_key)
            instance.delete()
            return JsonResponse({"message": "success"})



def check_user_has_access_to_trip(trip_id, request_user_id):
    this_trip = get_object_or_404(Trip, id=trip_id)
    this_trip_users = this_trip.groups.values('id')
    this_trip_users = [user['id'] for user in this_trip_users]
    if request_user_id in this_trip_users:
        return True
    else:
        return False

def add_expense(trip_id, request):
    this_trip = Trip.objects.get(pk=trip_id)
    expenses = Expenses(trip=this_trip,
                        expense=float(request.POST['expense']),
                        expense_type=request.POST['expense_type'],
                        description = request.POST['description'],
                        transaction_date = request.POST['transaction_date'] if request.POST['transaction_date'] != "" else None
    )
    expenses.save()