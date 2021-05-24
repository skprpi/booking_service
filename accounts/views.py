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


def get_time_price_list(disciplines):
    time_price = {}
    for el in disciplines:
        if el.name not in time_price:
            time_price[el.name] = []
        time_price[el.name].append(f'{el.duration} min - {el.price}')
    return time_price


def get_booked_times_list(lessons, count_load_days):
    booked_times = [[] for _ in range(count_load_days)]
    for el in lessons:
        time = el.start_datetime
        time = time.replace(tzinfo=None)

        delta = time - datetime.today().replace(minute=0, hour=0, second=0)

        day_idx = delta.days
        idx = (time.hour * 60 + time.minute + 1) // 15
        for i in range((el.duration + 1) // 15):
            booked_times[day_idx].append(idx + i)
    return booked_times


def get_lessons_obj(user_id, count_load_days):
    start_date = datetime.today().replace(minute=0, hour=0, second=0)
    end_date = start_date + timedelta(days=count_load_days)
    lessons = Lesson.objects.filter(
        student_pk=user_id,
        start_datetime__range=[start_date, end_date],
    ) | Lesson.objects.filter(
        teacher_pk=user_id,
        start_datetime__range=[start_date, end_date]
    )
    return lessons


def get_date_week_month(count_load_days):
    week_days_names = ['-', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    month_names = ['-', 'январь', 'февраль', 'март', 'аперь', 'май', 'июнь',
                   'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь',
                   'декабрь']
    week_days = ['' for _ in range(count_load_days)]
    date_number = [0 for _ in range(count_load_days)]
    month_number = ['' for _ in range(count_load_days)]
    for i in range(count_load_days):
        delta = timedelta(days=i)
        next_day = datetime.today() + delta
        day_idx = next_day.isoweekday()
        week_days[i] = week_days_names[day_idx]
        date_number[i] = next_day.day
        month_number[i] = month_names[next_day.month]
    return date_number, week_days, month_number


def home(request, teacher_pk):
    count_load_days = 30
    start_show_time = 10
    end_show_time = 23

    teacher = get_object_or_404(User, pk=teacher_pk)
    if teacher.role != UserRoles.TEACHER or request.user.role != UserRoles.STUDENT:
        return
    lessons = get_lessons_obj(request.user.id, count_load_days)
    disciplines = DisciplineDescription.objects.filter(teacher_pk=teacher_pk)
    date_number, week_days, month_number = get_date_week_month(count_load_days)

    user_context = {
        'pk': request.user.id,
        'text': get_object_or_404(User, pk=request.user.id).email,
        'lessons': lessons,
        'teacher_name': teacher.name,
        'teacher_surname': teacher.surname,
        'time_price': get_time_price_list(disciplines),
        'load_days_range': range(count_load_days),
        'booked_times': get_booked_times_list(lessons, count_load_days),
        'time_range': range(start_show_time, end_show_time + 1),
        'count_cell_in_row': range(4),
        'week_days': week_days,
        'date_number': date_number,
        'month_number': month_number,
    }
    return render(request, 'home.html', context=user_context)
