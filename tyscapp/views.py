from pyexpat.errors import messages
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from tyscapp.models import User, Contact, Event, Tickets

# Create your views here.
def index(request):
    return render(request, "index.html")
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('/loginPage')
    
    context = {"form": form}
    return render(request, "auth/register.html", context)



@login_required(login_url='/loginPage')
def dashboard(request):
    
    context = {
        "all_tickets": Tickets.objects.all(),
    }
    return render(request, "dashboard.html", context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('dashboard')
        else:
            messages.info(request, 'Username OR password is incorrect')
             
    
    return render(request, "auth/login.html")


@login_required(login_url='/loginPage')
def logoutUser(request):
    logout(request)
    return HttpResponseRedirect('loginPage')


def contact(request):
    
    return render(request, "contact.html")
def create_contact(request):
    if request.method == 'POST':
        errors = Contact.objects.basic_validator(request.POST)
    
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/contact")
    name_from_form = request.POST['name']
    email_from_form = request.POST['email']
    message_from_form = request.POST['message']
    context = Contact.objects.create(name=name_from_form, email=email_from_form, message=message_from_form)
    return redirect("/thanks")

def thanks(request):
        
        return render(request, "thanks.html")

def schedule(request):
    context = {
        "all_events": Event.objects.all(),
    }
    
    return render(request, "schedule.html", context)
def roster(request):
    
    return render(request, "roster.html")

@login_required(login_url='/loginPage')
def create_event_user(request):
    if request.method == 'POST':
        errors = Tickets.objects.basic_validator(request.POST)
        
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return HttpResponseRedirect("tickets")
    
    other_model = Event.objects.get(id=request.POST['event_id'])
    section_from_form = request.POST['section']
    number_from_form = request.POST['number']
    context = Tickets.objects.create(section=section_from_form, number=number_from_form, event=other_model, user=request.user)
    return HttpResponseRedirect("dashboard")

@login_required(login_url='/loginPage')
def tickets(request):
    
    context = {
        'all_events': Event.objects.all(),
    }
    
    return render(request, "tickets.html", context)

@login_required(login_url='/loginPage')
def view_ticket(request, ticket_id):
    context = {
        'ticket': Tickets.objects.get(id=ticket_id),
        'all_events': Event.objects.all(),
    }
    
    return render(request,"view_ticket.html" , context)

@login_required(login_url='/loginPage')
def edit_ticket(request, ticket_id):
    if request.method == 'POST':
        errors = Tickets.objects.basic_validator(request.POST)
        
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return HttpResponseRedirect(f"/edit_ticket/{ticket_id}")
    context = {
        'ticket': Tickets.objects.get(id=ticket_id),
        'all_events': Event.objects.all(),
    }
    
    if request.method == 'POST':
        ticket_to_update = Tickets.objects.get(id=ticket_id)
        ticket_to_update.section = request.POST['section']
        ticket_to_update.number = request.POST['number']
        ticket_to_update.event = Event.objects.get(id=request.POST['event_id'])
        ticket_to_update.save()
        return HttpResponseRedirect("/dashboard")
        
    return render(request,"edit_ticket.html" , context)

    
@login_required(login_url='/loginPage')
def delete_ticket(request, ticket_id):
    ticket_to_delete = Tickets.objects.get(id=ticket_id)
    ticket_to_delete.delete()
    return HttpResponseRedirect("/dashboard")