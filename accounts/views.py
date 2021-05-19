from django.contrib.auth import login, get_user_model
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserLoginForm, UserRegisterForm
from .models import UserRoles, Lesson

User = get_user_model()


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home', pk=request.user.id)
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def home(request, pk):
    lessons = Lesson.objects.filter(student_pk=request.user.id) | Lesson.objects.filter(teacher_pk=request.user.id)
    print(lessons)
    user_context = {'pk': request.user.id, 'text': get_object_or_404(User, pk=request.user.id).email, 'lessons': lessons}
    if request.user.role != UserRoles.ADMIN and request.user.id != pk:
        return render(request, 'home.html', context=user_context)
    admin_context = {'pk': pk, 'text': get_object_or_404(User, pk=pk).email, 'lessons': lessons}
    return render(request, 'home.html', context=admin_context)
