from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('dashboard', views.dashboard),
    path('login', views.login),
    path('logoutUser', views.logoutUser),
    path('schedule', views.schedule),
    path('roster', views.roster),
    path('contact', views.contact),
    path('create_contact', views.create_contact),
    path('tickets', views.tickets),
    path('loginPage', views.loginPage),
    path('create_event_user', views.create_event_user),
    path('edit_ticket/<int:ticket_id>', views.edit_ticket, name='edit_ticket'),
    path('delete_ticket/<int:ticket_id>', views.delete_ticket, name='delete_ticket'),
    path('view_ticket/<int:ticket_id>', views.view_ticket, name='view_ticket'),
    path('thanks', views.thanks),
    
    
] 