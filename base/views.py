from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .models import Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class CustomeLoginView(LoginView):
    template_name ="base/login.html"
    redirect_authenticated_user= True

    def get_success_url(self):
        return reverse_lazy('tasks')
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class =UserCreationForm
    redirect_authenticated_user= True
    success_url  =reverse_lazy("tasks")
    

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)
    

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"

    def get_queryset(self):
        # Get the base queryset (tasks belonging to the current user)
        queryset = Task.objects.filter(user=self.request.user)
        
        # Check if there's a search input from the GET request
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            # Filter the queryset based on the search input
            queryset = queryset.filter(title__icontains=search_input)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the total tasks, completed tasks, and pending tasks
        total_tasks = self.get_queryset().count()
        pending_tasks = self.get_queryset().filter(complete=False).count()
        completed_tasks = self.get_queryset().filter(complete=True).count()

        # Add these values to the context
        context["total_tasks"] = total_tasks
        context["pending_tasks"] = pending_tasks
        context["completed_tasks"] = completed_tasks
        
        # Add the search input back to the context to display it in the template
        context['search_input'] = self.request.GET.get('search-area') or ''
        
        return context

    

class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = "task"
    template_name = "base/task.html"

class TaskCreate(CreateView):  
    model =Task
    # form_class =forms.modelform_factory(Task, fields=['title', 'description'])
    fields = ['title', 'description', 'complete']
    success_url  =reverse_lazy("tasks")

    def form_valid(self, form):
        # Set the user as the currently logged-in user
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(UpdateView):
    model =Task
    fields = ['title', 'description', 'complete']
    success_url  =reverse_lazy("tasks")

class TaskDelete(DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("tasks")