from datetime import datetime, timedelta

from django.contrib.auth import login, get_user_model
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserLoginForm, UserRegisterForm
from .models import UserRoles, Lesson, DisciplineDescription

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
    lessons = Lesson.objects.filter(
        student_pk=request.user.id) | Lesson.objects.filter(
        teacher_pk=request.user.id)
    n = 30
    user_context = {'pk': request.user.id,
                    'text': get_object_or_404(User, pk=request.user.id).email,
                    'lessons': lessons, 'n': range(30)}
    if request.user.role != UserRoles.ADMIN and request.user.id != pk:
        return render(request, 'home.html', context=user_context)
    admin_context = {'pk': pk, 'text': get_object_or_404(User, pk=pk).email,
                     'lessons': lessons, 'n': range(30)}
    return render(request, 'home.html', context=admin_context)


def home2(request, teacher_pk):
    teacher = get_object_or_404(User, pk=teacher_pk)
    if teacher.role != UserRoles.TEACHER or request.user.role != UserRoles.STUDENT:
        return

    startdate = datetime.today().replace(minute=0, hour=0, second=0)
    enddate = startdate + timedelta(days=120)

    lessons = Lesson.objects.filter(student_pk=request.user.id,
                                    start_datetime__range=[startdate,
                                                           enddate]) | Lesson.objects.filter(
        teacher_pk=request.user.id, start_datetime__range=[startdate, enddate])
    disciplines = DisciplineDescription.objects.filter(teacher_pk=teacher_pk)
    time_price = {}
    for el in disciplines:
        if el.name not in time_price:
            time_price[el.name] = []
        time_price[el.name].append(f'{el.duration} min - {el.price}')
    print(time_price)

    booked_times = [[] for _ in range(30)]
    for el in lessons:
        time = el.start_datetime
        time = time.replace(tzinfo=None)

        delta = time - datetime.today().replace(minute=0, hour=0, second=0)

        day_idx = delta.days
        idx = (time.hour * 60 + time.minute + 1) // 15
        for i in range((el.duration + 1) // 15):
            booked_times[day_idx].append(idx + i)

    week_days_names = ['-', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    month_names = ['-', 'январь','февраль','март','аперь','май','июнь','июль','август','сентябрь','октябрь', 'ноябрь', 'декабрь']
    week_days = ['' for _ in range(30)]
    date_number = [0 for _ in range(30)]
    month_number = ['' for _ in range(30)]
    for i in range(30):
        delta = timedelta(days=i)
        next_day = datetime.today() + delta
        day_idx = next_day.isoweekday()
        week_days[i] = week_days_names[day_idx]
        date_number[i] = next_day.day
        month_number[i] = month_names[next_day.month]

    print(week_days)

    user_context = {
        'pk': request.user.id,
        'text': get_object_or_404(User, pk=request.user.id).email,
        'lessons': lessons,
        'teacher_name': teacher.name,
        'teacher_surname': teacher.surname,
        'time_price': time_price,
        'n': range(30),
        'booked_times': booked_times,
        'time_range': range(10, 23),
        'n2': [0, 1, 2, 3],
        'week_days': week_days,
        'date_number': date_number,
        'month_number': month_number,
    }
    return render(request, 'home.html', context=user_context)
