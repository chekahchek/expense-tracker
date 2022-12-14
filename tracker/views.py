from django.shortcuts import render
from tracker.models import Trip, Group, Expenses, Tags, Blog, Comment
from django.db.models import Sum
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from django.urls import reverse_lazy, reverse
from tracker.forms import CreateTripForm, ShareTripForm, AddExpenseForm, CreateBlogForm, CommentForm
from django.core.paginator import Paginator
from tracker.utils import UpdateBaseClass, check_user_has_access_to_trip, add_expense, DeleteBaseClass


class HomeView(View):
    def get(self, request):
        _url = '/accounts/login/?next=' + reverse('tracker:trip_list') #accounts/login/?next=/trip
        return redirect(_url)


class ShareTripView(LoginRequiredMixin, View):
    template_name = 'tracker/share_trip.html'

    def get(self, request, pk):
        user_can_access = check_user_has_access_to_trip(trip_id=pk, request_user_id=request.user.id)
        if user_can_access:
            username_invalid = request.session.get('username_invalid', False)
            if ( username_invalid ) : del(request.session['username_invalid'])
            this_trip = Trip.objects.get(pk=pk)
            form = ShareTripForm()
            ctx = {'form' : form, 'trip': this_trip, 'username_invalid': username_invalid}
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


#************************************************* TRIP *************************************************************
class TripListView(LoginRequiredMixin, ListView):
    template_name = 'tracker/trip_list.html'

    def get(self, request):
        trip_list = list()
        form = CreateTripForm()
        if request.user.is_authenticated:
            try:
                trip_list = Trip.objects.filter(groups__in=[request.user.id]) #Get all the trips thtat user has access to
            except:
                pass #If user has no trip, then pass in an empty list
        ctx = {'trip_list' : trip_list, 'form' : form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None): #When user creates a new trip
        this_trip = Trip(title=request.POST['title'],
                         budget=request.POST['budget'] if request.POST['budget'] != "" else None,
                         depart_date=request.POST['depart_date'] if request.POST['depart_date'] != "" else None,
                         return_date=request.POST['return_date'] if request.POST['return_date'] != "" else None,
        )

        this_trip.save()
        this_trip.groups.add(request.user)
        return redirect(reverse('tracker:trip_list'))


class TripUpdate(UpdateBaseClass): #When user updates his trip information
    def __init__(self):
        model = Trip
        modelform = CreateTripForm
        modelname = 'trip'
        super(UpdateBaseClass, self).__init__(model=model, modelform=modelform, modelname=modelname)


class TripDelete(DeleteBaseClass): #When user deletes the entire trip
    def __init__(self):
        model = Trip
        modelname = 'CreateTripForm'
        super(DeleteBaseClass, self).__init__(model=model, modelname=modelname)


#************************************ EXPENSES **********************************************************
class TripDetaiView(LoginRequiredMixin, DetailView): #Trip expenses overall view
    template_name = 'tracker/trip_detail.html'

    def get(self, request, pk): #Get the aggregated information of the trip expenses
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

    def post(self, request, pk): #When user adds in new expenses for the trip
        add_expense(trip_id=pk, request=request)
        return redirect(reverse('tracker:trip_detail', args=[pk]))

class TripExpense(LoginRequiredMixin, DetailView): #List of all the expenses of the trip
    template_name = 'tracker/trip_expense.html'

    def get(self, request, pk, expense_id=None): #Get all the expenses for the trip
        user_can_access = check_user_has_access_to_trip(trip_id=pk, request_user_id=request.user.id)
        if user_can_access:
            this_trip = Trip.objects.get(pk=pk)
            form = AddExpenseForm()
            all_expenses = Expenses.objects.filter(trip=this_trip).order_by('id').reverse() #Reverse so that the latest entry appears at the top
            paginator = Paginator(all_expenses, 25)
            page_num = request.GET.get('page')
            page_obj = paginator.get_page(page_num)
            ctx = {'trip': this_trip, 'form': form, 'page_obj': page_obj}
            return render(request, self.template_name, ctx)
        else:
            raise Http404('Access denied')

    def post(self, request, pk): #When user adds in new expenses for the trip
        add_expense(trip_id=pk, request=request)
        return redirect(reverse('tracker:trip_expense', args=[pk]))


class TripExpenseUpdate(UpdateBaseClass): #When user update the expenses for the trip
    def __init__(self):
        model = Expenses
        modelform = AddExpenseForm
        modelname = 'expense'
        super(UpdateBaseClass, self).__init__(model=model, modelform=modelform, modelname=modelname)


class TripExpenseDelete(DeleteBaseClass): #When user deletes any expenses for the trip
    def __init__(self):
        model = Expenses
        modelname = 'expense'
        super(DeleteBaseClass, self).__init__(model=model, modelname=modelname)


#*************************************** BLOG *******************************************************
class TripBlog(LoginRequiredMixin, DetailView): #List of all the blog entries for the trip
    template_name = 'tracker/trip_blog.html'

    def get(self, request, pk): #Get all the blog entries associated with the trip
        user_can_access = check_user_has_access_to_trip(trip_id=pk, request_user_id=request.user.id)
        if user_can_access:
            this_trip = Trip.objects.get(pk=pk)
            blog_posts = Blog.objects.filter(trip=this_trip).order_by('id').reverse()
            ctx = {'trip': this_trip, 'blog_posts' : blog_posts}
            return render(request, self.template_name, ctx)
        else:
            raise Http404('Access denied')

class TripBlogCreate(LoginRequiredMixin, DetailView): #Create a blog entry using the traditional way rather than using modal/Ajax since it is easy to close the modal and discard changes
    template_name = 'tracker/create_blog_entry.html'

    def get(self, request, pk):
        user_can_access = check_user_has_access_to_trip(trip_id=pk, request_user_id=request.user.id)
        if user_can_access:
            this_trip = Trip.objects.get(pk=pk)
            form = CreateBlogForm()
            ctx = {'trip': this_trip, 'form' : form}
            return render(request, self.template_name, ctx)
        else:
            raise Http404('Access denied')

    def post(self, request, pk):
        this_trip = Trip.objects.get(pk=pk)
        blog = Blog(trip=this_trip,
                    title=(request.POST['title']),
                    post=request.POST['post'],
                    )
        blog.save()
        return redirect(reverse('tracker:trip_blog', args=[pk]))

class TripBlogUpdate(LoginRequiredMixin, DetailView): #Update the blog entry
    template_name = 'tracker/create_blog_entry.html'

    def get(self, request, pk, blog_id):
        user_can_access = check_user_has_access_to_trip(trip_id=pk, request_user_id=request.user.id)
        if user_can_access:
            this_trip = Trip.objects.get(pk=pk)
            entry = get_object_or_404(Blog, id=blog_id)
            form = CreateBlogForm(instance=entry)
            ctx = {'form' : form, 'trip' : this_trip}
            return render(request, self.template_name, ctx)


    def post(self, request, pk, blog_id):
        entry = get_object_or_404(Blog, id=blog_id)
        form = CreateBlogForm(request.POST, instance=entry)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        entry = form.save()
        return redirect(reverse('tracker:trip_blog', args=[pk]))


class TripBlogDelete(DeleteBaseClass): #Delete the blog entry
    def __init__(self):
        model = Blog
        modelname = 'blog'
        super(DeleteBaseClass, self).__init__(model=model, modelname=modelname)


class BlogDetailView(LoginRequiredMixin, DetailView): #Show the full contents of the blog entry
    template_name = 'tracker/blog_detail.html'

    def get(self, request, pk, blog_id):
        user_can_access = check_user_has_access_to_trip(trip_id=pk, request_user_id=request.user.id)
        if user_can_access:
            this_trip = Trip.objects.get(pk=pk)
            entry = get_object_or_404(Blog, id=blog_id)
            comments = Comment.objects.filter(blogpost=entry).order_by('created_at').reverse()
            form = CommentForm()
            ctx = {'trip': this_trip, 'form': form, 'blog': entry, 'comments':comments}
            return render(request, self.template_name, ctx)


    def post(self, request, pk, blog_id): #Adding in comments associated with the blog entry
        blogpost = Blog.objects.get(pk=blog_id)
        comment = Comment(text = request.POST['text'],
                          blogpost = blogpost,
                          owner = request.user)
        comment.save()
        return redirect(reverse('tracker:blog_detail', args=[pk, blog_id]))


class CommentDelete(DeleteBaseClass):
    def __init__(self):
        model = Comment
        modelname = 'comment'
        super(DeleteBaseClass, self).__init__(model=model, modelname=modelname)


"""
Additional notes:
- this_trip is passed in since base_sidebar requires 'trip.id' for navigation
- For classes that extended from DeleteBaseClass, we don't need to explicitly pass in the blog_id/expense_id into kwargs. The URL contains blog_id/expense_id which will be passed in
  as a parameter in the GET/POST method.
"""
