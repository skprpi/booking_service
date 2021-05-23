from django.contrib.auth import login, get_user_model
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserLoginForm, UserRegisterForm
from .models import UserRoles, Lesson, PriceDiscipline, Discipline, DisciplineDescription

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
    n = 30
    user_context = {'pk': request.user.id, 'text': get_object_or_404(User, pk=request.user.id).email, 'lessons': lessons, 'n': range(30)}
    if request.user.role != UserRoles.ADMIN and request.user.id != pk:
        return render(request, 'home.html', context=user_context)
    admin_context = {'pk': pk, 'text': get_object_or_404(User, pk=pk).email, 'lessons': lessons, 'n': range(30)}
    return render(request, 'home.html', context=admin_context)


# pk - id у кого смотрю расписание
def home2(request, teacher_pk):
    teacher = get_object_or_404(User, pk=teacher_pk)
    if teacher.role != UserRoles.TEACHER or request.user.role != UserRoles.STUDENT:
        return

    lessons = Lesson.objects.filter(student_pk=request.user.id) | Lesson.objects.filter(teacher_pk=request.user.id)
    disciplines = DisciplineDescription.objects.filter(teacher_pk=teacher_pk)
    time_price = {}
    for el in disciplines:
        if el.name not in time_price:
            time_price[el.name] = []
        time_price[el.name].append(f'{el.duration} min - {el.price}')
    print(time_price)


    p = [[40, 41, 42, 43, 56, 57, 58], [63, 64, 65],[53, 54, 55],[]]



    user_context = {
        'pk': request.user.id,
        'text': get_object_or_404(User, pk=request.user.id).email,
        'lessons': lessons,
        'teacher_name': teacher.name,
        'teacher_surname': teacher.surname,
        'time_price': time_price,
        'n': range(30),
        'p': p,
        'time_range': range(10, 23),
        'n2': [0, 1, 2, 3]
    }
    return render(request, 'home.html', context=user_context)
