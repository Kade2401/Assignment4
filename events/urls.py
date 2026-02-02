
from django.urls import path
from . import views
urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create/', views.create_event, name='create_event'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('<int:event_id>/register/', views.register_attendee, name='register_attendee'),
    path('attendee/<int:attendee_id>/remove/', views.remove_attendee, name='remove_attendee'),
    path('api/events/', views.api_event_list),
    path('api/events/create/', views.api_create_event),
    path('profile/', views.profile, name='profile'),
    path("register/", views.register, name="register"),path("api/events/", views.api_event_list),
    path("api/events/<int:event_id>/", views.api_update_event),
    path("api/events/<int:event_id>/delete/", views.api_delete_event),
]