from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Request, Category
from .forms import RequestForm, CategoryForm
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RequestSerializer, RequestPartialUpdateSerializer


def index(request):
    completed_requests = Request.objects.filter(status='completed').order_by('-created_at')[:4]
    in_progress_count = Request.objects.filter(status='in_progress').count()
    return render(request, 'index.html', {
        'completed_requests': completed_requests,
        'in_progress_count': in_progress_count
    })


@login_required
def application_list(request):
    user_requests = Request.objects.filter(user=request.user)
    status_filter = request.GET.get('status')

    if status_filter == 'new':
        user_requests = user_requests.filter(status='new')
    elif status_filter == 'in_progress':
        user_requests = user_requests.filter(status='in_progress')
    elif status_filter == 'completed':
        user_requests = user_requests.filter(status='completed')

    context = {
        'requests': user_requests
    }
    return render(request, 'application_list.html', context)


@login_required
def application_create(request):
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('application_list')
    else:
        form = RequestForm()

    return render(request, 'application_create.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@staff_member_required
def change_category(request):
    categories = Category.objects.all()
    return render(request, 'change_category.html', {'categories': categories})


@staff_member_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('change_category')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})


@staff_member_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('change_category')
    return render(request, 'delete_category.html', {'category': category})


@login_required
def dashboard(request):
    user_role = 'Администратор' if request.user.is_staff else 'Пользователь'
    return render(request, 'dashboard.html', {
        'user_role': user_role
    })


@staff_member_required
def change_application_status(request, pk):
    request_obj = get_object_or_404(Request, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status == 'in_progress':
            request_obj.status = 'in_progress'
            request_obj.save()
            return redirect('change_application')
        elif new_status == 'completed':
            if 'completed_image' in request.FILES:
                request_obj.status = 'completed'
                request_obj.image = request.FILES['completed_image']
                request_obj.save()
                return redirect('change_application')
            else:
                return render(request, 'change_application_status.html', {
                    'request_obj': request_obj,
                    'error': 'Для статуса «Выполнено» необходимо прикрепить изображение.'
                })

    return render(request, 'change_application_status.html', {
        'request_obj': request_obj
    })


@staff_member_required
def change_application(request):
    requests = Request.objects.all().order_by('-created_at')
    return render(request, 'change_application.html', {'requests': requests})


@login_required
def delete_application(request, pk):
    request_obj = get_object_or_404(Request, pk=pk, user=request.user)

    if request.method == 'POST':
        request_obj.delete()
        return redirect('application_list')

    return redirect('application_list')


class RequestListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        requests = Request.objects.all()
        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class RequestRetrieveUpdateDestroyView(APIView):
    def get(self, request, pk):
        request_obj = Request.objects.get(pk=pk)
        serializer = RequestSerializer(request_obj)
        return Response(serializer.data)

    def patch(self, request, pk):
        request_obj = Request.objects.get(pk=pk)
        serializer = RequestPartialUpdateSerializer(request_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        request_obj = Request.objects.get(pk=pk)
        request_obj.delete()
        return Response(status=204)


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
