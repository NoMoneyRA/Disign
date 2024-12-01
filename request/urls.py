from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('application_list/', views.application_list, name='application_list'),
    path('application_create/', views.application_create, name='application_create'),
    path('register/', views.register, name='register'),
    path('application/delete/<int:pk>/', views.delete_application, name='delete_application'),
    path('category/', views.change_category, name='change_category'),
    path('category/add/', views.add_category, name='add_category'),
    path('category/delete/<int:pk>/', views.delete_category, name='delete_category'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('request/change_application_status/<int:pk>/', views.change_application_status, name='change_application_status'),
    path('request/', views.change_application, name='change_application'),

    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/requests/', views.RequestListCreateView.as_view(), name='request-list-create'),
    path('api/requests/<int:pk>/', views.RequestRetrieveUpdateDestroyView.as_view(), name='request-detail'),
    ]