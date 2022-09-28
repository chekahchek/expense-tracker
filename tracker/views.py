from django.shortcuts import render
from tracker.models import Trip, Group, Expenses, Tags, Blog, Comment
from django.db.models import Sum
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from django.urls import reverse_lazy, reverse
from tracker.forms import CreateTripForm, ShareTripForm, AddExpenseForm
from django.core.paginator import Paginator

class CreateTripView(LoginRequiredMixin, View):
    template_name = 'tracker/create_trip.html'

    def get(self, request, pk=None):
        form = CreateTripForm()
        ctx = {'form' : form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        this_trip = Trip(title=request.POST['title'],
                         budget=request.POST['budget'] if request.POST['budget'] != "" else None,
                         depart_date=request.POST['depart_date'] if request.POST['depart_date'] != "" else None,
                         return_date=request.POST['return_date'] if request.POST['return_date'] != "" else None,
        )

        this_trip.save()
        this_trip.groups.add(request.user)
        return redirect(reverse('tracker:trip_list'))

class ShareTripView(LoginRequiredMixin, View):
    template_name = 'tracker/share_trip.html'

    def get(self, request, pk):
        user_can_access = check_user_has_access_to_trip(trip_id=pk, request_user_id=request.user.id)
        if user_can_access:
            username_invalid = request.session.get('username_invalid', False)
            if ( username_invalid ) : del(request.session['username_invalid'])
            form = ShareTripForm()
            ctx = {'form' : form, 'trip_id': pk, 'username_invalid': username_invalid}
            return render(request, self.template_name, ctx)
        else:
            raise Http404('Access denied')

    def post(self, request, pk):
        username = request.POST['username']
        try:
            user_id = User.objects.get(username=username).id
            this_trip = get_object_or_404(Trip, id=pk)
            this_trip.groups.add(user_id)
            return redirect(reverse('tracker:trip_detail', args=[pk]))

        except: #When the username keyed in is not valid
            request.session['username_invalid'] = True
            return redirect(reverse('tracker:share_trip', args=[pk]))


class HomeView(View):
    def get(self, request):
        _url = '/accounts/login/?next=' + reverse('tracker:trip_list') #accounts/login/?next=/trip
        return redirect(_url)

class TripListView(LoginRequiredMixin, ListView):
    template_name = 'tracker/trip_list.html'
    def get(self, request):
        trip_list = list()
        if request.user.is_authenticated:
            try:
                trip_list = Trip.objects.filter(groups__in=[request.user.id])
            except:
                pass
        ctx = {'trip_list' : trip_list}
        return render(request, self.template_name, ctx)


class TripDetaiView(LoginRequiredMixin, DetailView):
    template_name = 'tracker/trip_detail.html'

    def get(self, request, pk):
        user_can_access = check_user_has_access_to_trip(trip_id=pk, request_user_id=request.user.id)
        if user_can_access:
            form = AddExpenseForm()
            this_trip = Trip.objects.get(pk=pk)
            total_expense = Expenses.objects.filter(trip=this_trip).aggregate(Sum('expense'))
            expense_breakdown = Expenses.objects.filter(trip=this_trip).values('expense_type').annotate(total_expense=Sum('expense'))
            ctx = {'trip_id': pk, 'form': form, 'trip':this_trip, 'total_expense':total_expense, 'expense_breakdown':expense_breakdown}
            return render(request, self.template_name, ctx)
        else:
            raise Http404('Access denied')

    def post(self, request, pk):
        add_expense(trip_id=pk, request=request)
        return redirect(reverse('tracker:trip_detail', args=[pk]))

class TripExpense(LoginRequiredMixin, DetailView):
    template_name = 'tracker/trip_expense.html'

    def get(self, request, pk, expense_id=None):
        user_can_access = check_user_has_access_to_trip(trip_id=pk, request_user_id=request.user.id)
        if user_can_access:
            this_trip = Trip.objects.get(pk=pk)
            form = AddExpenseForm()
            all_expenses = Expenses.objects.filter(trip=this_trip).order_by('id').reverse()
            paginator = Paginator(all_expenses, 5)
            page_num = request.GET.get('page')
            page_obj = paginator.get_page(page_num)
            ctx = {'trip': this_trip, 'form': form, 'page_obj': page_obj}
            return render(request, self.template_name, ctx)
        else:
            raise Http404('Access denied')

    def post(self, request, pk):
        add_expense(trip_id=pk, request=request)
        return redirect(reverse('tracker:trip_expense', args=[pk]))


class TripExpenseUpdate(LoginRequiredMixin, DetailView):
    template_name = 'tracker/trip_expense.html'

    def get(self, request, pk, expense_id):
        if request.is_ajax():
            return JsonResponse({"message":"success"})
        else:
            return Http404('Access denied')

    def post(self, request, pk, expense_id):
        if request.is_ajax():
            this_expense = Expenses.objects.get(pk=expense_id)
            form = AddExpenseForm(request.POST or None, instance=this_expense)
            if form.is_valid():
                this_expense = form.save()
                return JsonResponse({"message": "success"})
            else:
                return JsonResponse({"message": "Validation failed"})
        else:
            return JsonResponse({"message": "Wrong request"})

class TripBlog(LoginRequiredMixin, DetailView):
    template_name = 'tracker/trip_blog.html'

    def get(self, request, pk):
        user_can_access = check_user_has_access_to_trip(trip_id=pk, request_user_id=request.user.id)
        if user_can_access:
            this_trip = Trip.objects.get(pk=pk)
            ctx = {'trip': this_trip}
            return render(request, self.template_name, ctx)
        else:
            raise Http404('Access denied')



#******************************************** COMMON UTILS ******************************************************
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


#Debugging
class Debugging(LoginRequiredMixin, View):
    template_name = 'tracker/debug.html'

    def get(self, request, pk=None):
        form = AddExpenseForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)